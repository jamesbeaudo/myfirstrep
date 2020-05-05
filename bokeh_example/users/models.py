from django.db import models
from django.contrib.auth.models import User, Group
from PIL import Image
from django.utils import timezone


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    #team=models.OneToOneField('auth.Group', unique=True, on_delete = models.CASCADE, default="team")
    team_num1 = models.CharField(max_length=30, null=True)
    
    testusercustomtitle = models.CharField(max_length=30, default="")

    #'17 data
    happiness17 = models.IntegerField(null=True, default=0)
    optimism17= models.IntegerField(null=True, default=0)
    sesteem17= models.IntegerField(null=True, default=0)
    emotion_reg17= models.IntegerField(null=True, default=0)
    impulse_ctrl17= models.IntegerField(null=True, default=0)
    stress_mgt17= models.IntegerField(null=True, default=0)
    empathy17= models.IntegerField(null=True, default=0)
    emotionperc17= models.IntegerField(null=True, default=0)
    emotion_exp17= models.IntegerField(null=True, default=0)
    relationship17=models.IntegerField(null=True, default=0)
    emotion_mgt17= models.IntegerField(null=True, default=0)
    assertive17= models.IntegerField(null=True, default=0)
    socialawa17= models.IntegerField(null=True, default=0)
    adaptability17= models.IntegerField(null=True, default=0)
    smotivation17=models.IntegerField(null=True, default=0)
    wellbeing17=models.IntegerField(null=True, default=0)
    scontrol17=models.IntegerField(null=True, default=0)
    emotionality17=models.IntegerField(null=True, default=0)
    socialibility17=models.IntegerField(null=True, default=0)
    
    #'18 data
    happiness18 = models.IntegerField(null=True, default=0)
    optimism18= models.IntegerField(null=True, default=0)
    sesteem18= models.IntegerField(null=True, default=0)
    emotion_reg18= models.IntegerField(null=True, default=0)
    impulse_ctrl18= models.IntegerField(null=True, default=0)
    stress_mgt18= models.IntegerField(null=True, default=0)
    empathy18= models.IntegerField(null=True, default=0)
    emotionperc18= models.IntegerField(null=True, default=0)
    emotion_exp18= models.IntegerField(null=True, default=0)
    relationship18=models.IntegerField(null=True, default=0)
    emotion_mgt18= models.IntegerField(null=True, default=0)
    assertive18= models.IntegerField(null=True, default=0)
    socialawa18= models.IntegerField(null=True, default=0)
    adaptability18= models.IntegerField(null=True, default=0)
    smotivation18=models.IntegerField(null=True, default=0)
    wellbeing18=models.IntegerField(null=True, default=0)
    scontrol18=models.IntegerField(null=True, default=0)
    emotionality18=models.IntegerField(null=True, default=0)
    socialibility18=models.IntegerField(null=True, default=0)

    #'19 data
    happiness19 = models.IntegerField(null=True, default=0)
    optimism19= models.IntegerField(null=True, default=0)
    sesteem19= models.IntegerField(null=True, default=0)
    emotion_reg19= models.IntegerField(null=True, default=0)
    impulse_ctrl19= models.IntegerField(null=True, default=0)
    stress_mgt19= models.IntegerField(null=True, default=0)
    empathy19= models.IntegerField(null=True, default=0)
    emotionperc19= models.IntegerField(null=True, default=0)
    emotion_exp19= models.IntegerField(null=True, default=0)
    relationship19=models.IntegerField(null=True, default=0)
    emotion_mgt19= models.IntegerField(null=True, default=0)
    assertive19= models.IntegerField(null=True, default=0)
    socialawa19= models.IntegerField(null=True, default=0)
    adaptability19= models.IntegerField(null=True, default=0)
    smotivation19=models.IntegerField(null=True, default=0)
    wellbeing19=models.IntegerField(null=True, default=0)
    scontrol19=models.IntegerField(null=True, default=0)
    emotionality19=models.IntegerField(null=True, default=0)
    socialibility19=models.IntegerField(null=True, default=0)
    
    #'20 data
    happiness20 = models.IntegerField(null=True, default=0)
    optimism20= models.IntegerField(null=True, default=0)
    sesteem20= models.IntegerField(null=True, default=0)
    emotion_reg20= models.IntegerField(null=True, default=0)
    impulse_ctrl20= models.IntegerField(null=True, default=0)
    stress_mgt20= models.IntegerField(null=True, default=0)
    empathy20= models.IntegerField(null=True, default=0)
    emotionperc20= models.IntegerField(null=True, default=0)
    emotion_exp20= models.IntegerField(null=True, default=0)
    relationship20=models.IntegerField(null=True, default=0)
    emotion_mgt20= models.IntegerField(null=True, default=0)
    assertive20= models.IntegerField(null=True, default=0)
    socialawa20= models.IntegerField(null=True, default=0)
    adaptability20= models.IntegerField(null=True, default=0)
    smotivation20=models.IntegerField(null=True, default=0)
    wellbeing20=models.IntegerField(null=True, default=0)
    scontrol20=models.IntegerField(null=True, default=0)
    emotionality20=models.IntegerField(null=True, default=0)
    socialibility20=models.IntegerField(null=True, default=0)
    
    #'21 data
    happiness21 = models.IntegerField(null=True, default=0)
    optimism21= models.IntegerField(null=True, default=0)
    sesteem21= models.IntegerField(null=True, default=0)
    emotion_reg21= models.IntegerField(null=True, default=0)
    impulse_ctrl21= models.IntegerField(null=True, default=0)
    stress_mgt21= models.IntegerField(null=True, default=0)
    empathy21= models.IntegerField(null=True, default=0)
    emotionperc21= models.IntegerField(null=True, default=0)
    emotion_exp21= models.IntegerField(null=True, default=0)
    relationship21=models.IntegerField(null=True, default=0)
    emotion_mgt21= models.IntegerField(null=True, default=0)
    assertive21= models.IntegerField(null=True, default=0)
    socialawa21= models.IntegerField(null=True, default=0)
    adaptability21= models.IntegerField(null=True, default=0)
    smotivation21=models.IntegerField(null=True, default=0)
    wellbeing21=models.IntegerField(null=True, default=0)
    scontrol21=models.IntegerField(null=True, default=0)
    emotionality21=models.IntegerField(null=True, default=0)
    socialibility21=models.IntegerField(null=True, default=0)
 
    d_uploaded = models.BooleanField(default=False)
    d_accessdata = models.BooleanField(default=False)
    d_makeemail= models.BooleanField(default=False)
    
    g_completedaily= models.BooleanField(default=False)
    g_preferences= models.BooleanField(default=False)
    g_setgoal= models.BooleanField(default=False)
    
    t_maketest= models.BooleanField(default=False)
    t_improve= models.BooleanField(default=False)
    
    #0 = Male, 1 = Female, 2=N/A
    gender=models.IntegerField(null=True, default=0)
    #0 = Intern, 1 = Entry-level, 2 = mid-level, 3 = manager, 4 = decision-maker
    experience=models.IntegerField(null=True, default=0)   
    areawork=models.CharField(max_length=30, default="")
    #0 = promotion, 1 = retirement, 2 = job security, 3 = self-development, 4 = flexibility
    aspirations=models.IntegerField(null=True, default=0)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
    
        img = Image.open(self.image.path)
    
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class TeamCreation(models.Model):

    team_name = models.CharField(max_length=100, default=None, unique=True)
    #group_id = models.IntegerField(max_length=6, default="")
    team_k = models.TextField(max_length=80, default="")
    date_posted = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.team_name
      

class Join(models.Model):

    team_name = models.CharField(max_length=100, default=None, unique=False)
    #group_id = models.IntegerField(max_length=6, default="")
    team_k = models.TextField(max_length=80, default="")

    def __str__(self):
        return self.team_name

    