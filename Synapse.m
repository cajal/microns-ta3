%{
# Anatomically localized synapse between two Segments
-> ta3.Segmentation
synapse_id               : int                           # synapse index within the segmentation
---

 (presyn) -> ta3.Segment
 (postsyn) -> ta3.Segment
synapse_x                   : float                         # 
synapse_y                   : float                         # 
synapse_z                   : float                         # 
%}


classdef Synapse < dj.Manual
end