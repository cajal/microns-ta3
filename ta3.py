# coding: utf-8


import datajoint as dj
dj.config['display.show_tuple_count'] = False


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
    key_point_x          : int                          # (um) 
    key_point_y          : int                          # (um)
    key_point_z          : int                          # (um)
    x_min                : int                          # (um) bounding box 
    y_min                : int                          # (um) bounding box
    z_min                : int                          # (um) bounding box
    x_max                : int                          # (um) bounding box
    y_max                : int                          # (um) bounding box
    z_max                : int                          # (um) bounding box
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
class Mesh(dj.Manual):
    definition = """
    # Trimesh of Segment
    -> Segment
    """
    
    class Fragment(dj.Part):
        definition = """
        # Mesh Fragment
        -> Mesh
        fragment             : smallint                     # fragment in mesh
        ---
        bound_x_min          : int                          # 
        bound_x_max          : int                          # 
        bound_y_min          : int                          # 
        bound_y_max          : int                          # 
        bound_z_min          : int                          # 
        bound_z_max          : int                          # 
        n_vertices           : int                          # number of vertices in this mesh
        n_triangles          : int                          # number of triangles in this mesh
        vertices             : longblob                     # x,y,z coordinates of vertices
        triangles            : longblob                     # triangles (triplets of vertices)
        """


@schema 
class Synapse(dj.Manual):
    definition = """
    # Anatomically localized synapse between two Segments
    -> Segmentation
    synapse_id        : bigint                     # synapse index within the segmentation
    ---
    (presyn) -> Segment
    (postsyn) -> Segment
    synapse_x            : float                        # 
    synapse_y            : float                        # 
    synapse_z            : float                        
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
