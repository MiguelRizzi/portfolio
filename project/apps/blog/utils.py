def validate_img_extension(file):
    try:
        ext = file.name.split('.')[-1]
        valid_extensions = ['jpg', 'jpeg', 'png', 'webp', 'gif']
        if ext.lower() in valid_extensions:
            return True
        else:
            return False
        
    except Exception:
        pass

    
def validate_video_extension(file):
    try:
        ext = file.name.split('.')[-1]
        valid_extensions = ['mp4', 'mov', 'avi', 'mkv', 'webm']
        if ext.lower() in valid_extensions:
            return True
        else:
            return False
    except Exception:
        pass