%{
# Segmentation iteration or snapshot
segmentation                : smallint                      # segmentation id
---
segmentation_description    : varchar(4000)                 # free text description of the segmentation
%}


classdef Segmentation < dj.Manual
end