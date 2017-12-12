%{
# Mesh Fragment
-> ta3.Mesh
fragment                    : smallint                      # fragment in mesh
---
bound_x_min                 : int                           # 
bound_x_max                 : int                           # 
bound_y_min                 : int                           # 
bound_y_max                 : int                           # 
bound_z_min                 : int                           # 
bound_z_max                 : int                           # 
n_vertices                  : int                           # number of vertices in this mesh
n_triangles                 : int                           # number of triangles in this mesh
vertices                    : longblob                      # x,y,z coordinates of vertices
triangles                   : longblob                      # triangles (triplets of vertices)
%}


classdef MeshFragment < dj.Manual
end