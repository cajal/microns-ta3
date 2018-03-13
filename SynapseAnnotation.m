%{
# 
-> ta3.Synapse
annotation_timestamp=CURRENT_TIMESTAMP: timestamp           # 
---
-> ta3.Proofreader
-> ta3.SynapseAnnotationLookup
annotation_comment          : varchar(4000)                 # 
%}


classdef SynapseAnnotation < dj.Manual
end