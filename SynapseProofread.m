%{
# 
-> ta3.Synapse
proofread_timestamp=CURRENT_TIMESTAMP: timestamp            # 
---
-> ta3.Proofreader
verdict                     : enum('valid','deprecated','ambiguous') # 
proofread_comment           : varchar(4000)                 # 
%}


classdef SynapseProofread < dj.Manual
end