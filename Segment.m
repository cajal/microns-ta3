%{
# Segment: a volumetric segmented object
-> ta3.Segmentation
segment_id                  : bigint                        # segment id unique within each Segmentation
---
boss_vset_id=null           : bigint unsigned               # IARPA's BOSS storage if applicable
key_point_x                 : int                           # (um)
key_point_y                 : int                           # (um)
key_point_z                 : int                           # (um)
x_min                       : int                           # (um) bounding box
y_min                       : int                           # (um) bounding box
z_min                       : int                           # (um) bounding box
x_max                       : int                           # (um) bounding box
y_max                       : int                           # (um) bounding box
z_max                       : int                           # (um) bounding box
%}


classdef Segment < dj.Manual
end