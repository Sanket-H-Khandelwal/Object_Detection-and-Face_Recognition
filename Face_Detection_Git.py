#!/usr/bin/env python
# coding: utf-8

# In[8]:


import boto3
#We will define the region_name, Access_Key,and aws_secret_access_key
def client_rekognition():
    client=boto3.client('rekognition',
                        region_name = 'region_name',
                        aws_access_key_id='Key_ID',
                        aws_secret_access_key='Access_Key')
    return client
    
#Now we will be creating a collection which will be used for the comparision 
def create_collection(collection_id):

    client=client_rekognition()
    #Create a collection
    print('Creating collection:' + collection_id)
    response=client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')
    
 #After the collection is created we will be adding faces to the collection   
def add_faces_to_collection(bucket,photo,collection_id):
    
    client=client_rekognition()

    response=client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                ExternalImageId=photo,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])

    print ('Results for ' + photo)
    print('Faces indexed:')
    
    for faceRecord in response['FaceRecords']:
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])
#After the collection is created and faces are added to the collection we will specify the source and the target file
def compare_faces(sourceFile, targetFile,bucket):

    client=client_rekognition()
    s3client = boto3.client('s3',
                            region_name='region_name',
                            aws_access_key_id='Key_ID',
                            aws_secret_access_key='Access_Key')
    
    imageSource=s3client.get_object(Bucket=bucket,Key=sourceFile)['Body']
    #imageSource=open(sourceFile,'rb')
    #imageTarget=open(targetFile,'rb')
    imageTarget=s3client.get_object(Bucket=bucket,Key=targetFile)['Body']

    response=client.compare_faces(SimilarityThreshold=98, # security perpose 98%
                                  SourceImage={'Bytes': imageSource.read()},
                                  TargetImage={'Bytes': imageTarget.read()})
    
    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        print('The face at ' +
               str(position['Left']) + ' ' +
               str(position['Top']) +
               ' matches with ' + similarity + '% confidence')

    imageSource.close()
    imageTarget.close()     
    return len(response['FaceMatches'])          


#We will pass the inormation about the collection_id, bucket name and photos that you want to compare.
    
def main():
    collection_id='PersonofInterest'
    create_collection(collection_id)
    bucket='Bucket_Name'
    photos=['xys.jpg','abc.JPG','pqr.jpg']
    #photo_path=['https://Bucket_Name.s3.us-east-2.amazonaws.com/xys.jpg',
    #'s3://Bucket_Name/abc.JPG',
    #            's3://Bucket_Name/pqr.jpg']
#This will initiate the face search and will return the image name if the similarity rate is greater than 98%    
    for i in range(len(photos)):
        indexed_faces_count=add_faces_to_collection(bucket,photo=photos[i],collection_id=collection_id)
        print("Faces indexed count: " + str(indexed_faces_count))
    
    print("Face Match starting ......")
    for i in range(len(photos)):
        source_file = photos[i]
        target_file='PersonofInterest.JPG'
        face_matches=compare_faces(source_file, target_file,bucket)
        if(face_matches >0):
            print("Face matches: " + photos[i])
            print("Person of Interest")
        elif (i==len(photos)):
            print(" Not a Person of Interest")
    
    

if __name__ == "__main__":
    main()    


# In[7]:


client=client_rekognition()
client.delete_collection(CollectionId='PersonofInterest')


# In[ ]:




