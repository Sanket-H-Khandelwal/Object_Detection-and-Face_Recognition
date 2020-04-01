# Face_Recognition


Project Background: 
Mass shooting is a bigger concern in the US and current security systems are not equipped to provide presence of criminals in the premises. If security officers can identify and notify presence of suspected criminals in premises, a preventive plan or measures can be taken by authorities to take strategic and operational actions. The whole idea is to reduce the response time so that the action can be taken quickly


Project Scope: 
Create a computer vision system using AWS services to detect wanted/person of interest and weapon with the help of  cctv camera.

Services used: S3, Amazon Rekognition, Amazon Sagemaker, IAM 

Wanted Person Detection: 
Use Case:
Any person who enters the building and crosses any cctv camera their faces are compared against the collection of wanted persons database and if  more than 98%  facial similarity is found, the image will be highlighted. 

Future Improvements
The current implementation is an MVP and all the code is written in Sagemaker. To improve security and architecture flexibility for future implementation, an layer of Lambda function will be implemented.
A server-client architecture with Edge computing can be used to ensure every CCTV can act independently, to wanted criminals.

