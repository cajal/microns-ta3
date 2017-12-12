%{
# 
-> ta3.Segment
annotation_timestamp=CURRENT_TIMESTAMP: timestamp           # 
---
-> ta3.Proofreader
-> ta3.AnnotationLookup
annotation_comment          : varchar(4000)                 # 
%}


classdef Annotation < dj.Manual
end