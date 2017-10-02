# coding: utf-8

import subprocess
import json
import time
import os
import datajoint as dj
import numpy as np

schema = dj.schema('microns_ta3', locals())
nda = dj.create_virtual_module('nda', 'microns_nda')

@schema
class Proofreader(dj.Lookup):
    definition = """
    # EM Segmentation proofreaders
    proofreader :  varchar(8)   # short name
    """
    contents = zip(('Tommy', 'Nick'))


@schema
class Segmentation(dj.Manual):
    definition = """
    # Segmentation iteration or snapshot
    segmentation  : smallint   # segmentation id
    ---
    segmentation_description : varchar(4000)   #  free text description of the segmentation
    """


@schema
class Segment(dj.Manual):
    definition = """
    # Segment: a volumetric segmented object
    -> Segmentation
    segment_id : bigint   # segment id unique within each Segmentation
    ---
    boss_vset_id=null    : bigint unsigned              # IARPA's BOSS storage if applicable
    """


@schema
class Proofread(dj.Manual):
    definition = """  #
    -> Segment
    proofread_timestamp = CURRENT_TIMESTAMP  : timestamp
    ---
    -> Proofreader
    verdict  : enum('valid', 'deprecated', 'ambiguous')
    proofread_comment=""  : varchar(4000)
    """

@schema
class AnnotationLookup(dj.Lookup):
    definition = """  # list of possible annotations
    annotation : varchar(255)
    """
    contents = zip(('spiny', 'sparsely spiny', 'aspiny', 'basket',
                    'Martinotti', 'bipolar', 'neurogliaform', 'chandelier',
                    'axon', 'dendrite', 'glia', 'vessel', 'astrocyte'))


@schema
class Annotation(dj.Manual):
    definition = """
    -> Segment
    annotation_timestamp = CURRENT_TIMESTAMP  : timestamp
    ---
    -> Proofreader
    -> AnnotationLookup
    annotation_comment  : varchar(4000)
    """



@schema
class Mesh(dj.Imported):

    path = 'gs://pinky_share/pinky40_v11/watershed_mst_trimmed_sem_remap/mesh_mip_3_err_40'

    definition = """
    -> Segment
    """

    class Fragment(dj.Part):
        definition = """ # Mesh Fragment
        -> Mesh
        fragment  : smallint   # fragment in mesh
        ----
        bound_x_min   : int
        bound_x_max   : int
        bound_y_min   : int
        bound_y_max   : int
        bound_z_min   : int
        bound_z_max   : int
        n_vertices  :  int     # number of vertices in this mesh
        n_triangles :  int     # number of triangles in this mesh
        vertices    :  longblob  # x,y,z coordinates of vertices
        triangles   :  longblob  # triangles (triplets of vertices)
        """

    def _make_tuples(self, key):

        def generate_fragments(manifest, key):
            for fragment, fname in enumerate(manifest['fragments']):
                boss_id, n, coords = fname.split(':')
                subprocess.run(['gsutil', 'cp', '%s/%s' % (Mesh.path, fname), 'data'], stdout=subprocess.PIPE)
                with open(os.path.join('data', fname), 'br') as f:
                    buffer = f.read()
                num_vertices = np.frombuffer(buffer[:4], dtype='uint32')[0]
                buffer = buffer[4:]
                vertices = np.frombuffer(buffer[:12*num_vertices], dtype='float32').reshape((num_vertices, 3))
                buffer = buffer[12*num_vertices:]
                num_triangles = len(buffer)//12
                triangles = np.frombuffer(buffer, dtype='uint32').reshape((num_triangles, 3))
                assert triangles.max() < 0xFFFF
                triangles = triangles.astype('uint16')
                bounds = list(map(int, coords.replace('_','-').split('-')))
                yield dict(key,
                           fragment=fragment,
                           bound_x_min=bounds[0],
                           bound_x_max=bounds[1],
                           bound_y_min=bounds[2],
                           bound_y_max=bounds[3],
                           bound_z_min=bounds[4],
                           bound_z_max=bounds[5],
                           n_vertices=num_vertices,
                           n_triangles=num_triangles,
                           vertices=vertices,
                           triangles=triangles)

        result = subprocess.run(['gsutil', 'cat', '%s/%d:0' % (Mesh.path, key['segment_id'])], stdout=subprocess.PIPE)
        manifest = json.loads(result.stdout)
        self.insert1(key)
        Mesh.Fragment().insert(generate_fragments(manifest, key))


@schema
class Synapse(dj.Manual):
    definition = """
    # Anatomically localized synapse between two Segments
    -> Segmentation
    synapse_id        : bigint                     # synapse index within the segmentation
    ---
    (presyn) -> Segment
    (postsyn) -> Segment
    synapse_x            : bigint    # (EM voxels)
    synapse_y            : bigint    # (EM voxels)
    synapse_z            : bigint    # (EM voxels)
    syn_bbox_x1          : bigint    # (EM voxels)  - bounding box
    syn_bbox_y1          : bigint    # (EM voxels)  - bounding box
    syn_bbox_z1          : bigint    # (EM voxels)  - bounding box
    syn_bbox_x2          : bigint    # (EM voxels)  - bounding box
    syn_bbox_y2          : bigint    # (EM voxels)  - bounding box
    syn_bbox_z2          : bigint    # (EM voxels)  - bounding box
    """


@schema
class SynapseProofread(dj.Manual):
    definition = """  #
    -> Synapse
    proofread_timestamp = CURRENT_TIMESTAMP  : timestamp
    ---
    -> Proofreader
    verdict  : enum('valid', 'deprecated', 'ambiguous')
    proofread_comment=""  : varchar(4000)
    """


@schema
class SynapseAnnotationLookup(dj.Lookup):
    definition = """  # list of possible annotations
    annotation : varchar(255)
    """
    contents = zip(('symmetric', 'asymmetric', 'ambiguous'))


@schema
class SynapseAnnotation(dj.Manual):
    definition = """
    -> Synapse
    annotation_timestamp = CURRENT_TIMESTAMP  : timestamp
    ---
    -> Proofreader
    -> SynapseAnnotationLookup
    annotation_comment  : varchar(4000)
    """


@schema
class Soma(dj.Manual):
    definition = """
    # A segment including a cell soma
    -> Segment
    ---
    -> nda.EMCell
    """


@schema
class Neurite(dj.Manual):
    definition = """
    # orphaned axon or dendrite
    -> Segment
    ---
    -> nda.Mask
    """
