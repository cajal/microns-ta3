
# coding: utf-8

# In[1]:


import datajoint as dj
dj.config['database.host'] = 'datajoint.ninai.org'
dj.config['database.user'] = 'dimitri'


# In[2]:


nda = dj.create_virtual_module('nda', 'microns_nda')


# In[3]:


schema = dj.schema('microns_ta3', locals())


# In[4]:


@schema
class Segmentation(dj.Manual):
    definition = """
    # Segmentation iteration or snapshot
    segmentation  : smallint   # segmentation id
    ---
    segmentation_description : varchar(4000)   #  free text description of the segmentation    
    """


# In[5]:


@schema
class Segment(dj.Manual):
    definition = """
    # Segment: a volumetric segmented object
    -> Segmentation
    segment_id : bigint   # segment id unique within each Segmentation
    ---
    boss_vset_id         : bigint unsigned              # 
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


# In[6]:


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


# In[7]:


@schema 
class Synapse(dj.Manual):
    definition = """
    # Anatomically localized synapse between two Segments
    -> Segmentation
    synapse_index        : int                     # synapse index within the segmentation
    ---
    (presyn) -> Segment
    (postsyn) -> Segment
    synapse_x            : float                        # 
    synapse_y            : float                        # 
    synapse_z            : float                        
    """


# In[8]:



@schema
class Soma(dj.Manual):
    definition = """
    # A segment including a cell soma
    -> Segment
    ---
    -> nda.EMCell
    """


# In[9]:


@schema
class Classification(dj.Lookup):
    definition = """
    # all possible cell types
    celltype : varchar(8)   # short name of cell type
    ---
    celltype_description : varchar(255)  # detailed description of cell type
    """

@schema 
class Class(dj.Manual):
    definition = """
    # Cell classification
    -> Segment
    -> Classification
    """
    
@schema
class Neurite(dj.Manual):
    definition = """
    # orphaned axon or dendrite
    -> Segment    
    ---
    -> nda.Mask
    """


# In[10]:


@schema
class ChangeLog(dj.Manual):
    definition = """
    log_entry    : serial 
    ---
    change_date  : date 
    -> Segmentation
    """


# In[11]:


dj.ERD(ta3) + dj.ERD(nda)


# In[ ]:


nda.Soma()


# In[ ]:




