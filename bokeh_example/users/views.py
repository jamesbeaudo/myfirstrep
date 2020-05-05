from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, TeamCreationForm, JoinForm, PreferencesForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import Group
from .models import TeamCreation, Profile
from django.contrib import admin
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfFileReader
import PyPDF2
import io
from bokeh.plotting import figure, output_file, show, reset_output
from bokeh.embed import components
from bokeh.transform import dodge, factor_cmap
from bokeh.models import (Range1d, ColumnDataSource, BasicTicker, ColorBar,LinearColorMapper, PrintfTickFormatter, SaveTool, PanTool, ResetTool,
                          ZoomInTool, BoxSelectTool, BoxZoomTool, HoverTool, RangeTool, ZoomOutTool, Button, CustomJS, DataTable, NumberFormatter,
                          RangeSlider, TableColumn, FactorRange, Toolbar,  ToolbarBox)
from PIL import ImageGrab
import pandas as pd
from bokeh.transform import transform, linear_cmap
from bokeh.layouts import column, row
from django.shortcuts import render_to_response
from os.path import dirname, join
from bokeh.io import curdoc
import csv
import numpy as np
from bokeh.util.hex import hexbin
from statistics import mean

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'pages/register.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'pages/profile.html', context)

@login_required
def create_team(request):
    if request.method=='POST':
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            newTeam = form.save(commit=False)


            if not TeamCreation.objects.filter(team_name=newTeam.team_name).exists():
                newTeam.save()
                #assign team
                group_name=newTeam.team_name            
                user = request.user
                user.profile.team_num1=group_name
                user.profile.save()
                newTeam.save()
                #redirect homepage
                team_name = form.cleaned_data.get('team_name')
                username = user.username
                messages.success(request, f'Successfully joined {team_name}! Welcome aboard {username}!')
                #set group name / future unique condition 
                new_group, created = Group.objects.get_or_create(name=newTeam.team_name)
                newTeam.save() 
                return redirect('dashboard')
            
            else:

                messages.error(request, f'Please try again, this team exists')

    else:
        form=TeamCreationForm()

    context={
            "form":form,
            }
    
    return render(request, "pages/team_creation.html", context)

@login_required
def join_team(request):
    
        context={
                }
        
        return render(request, "pages/join_team.html", context)

@login_required
def storytelling(request):
        user = request.user
        d_upload=user.profile.d_uploaded
        d_access=user.profile.d_accessdata
        d_email=user.profile.d_makeemail
        g_daily=user.profile.g_completedaily
        g_pref=user.profile.g_preferences
        g_goal=user.profile.g_setgoal
        t_test=user.profile.t_maketest
        t_imp=user.profile.t_improve
        if request.method=='POST':
            form = JoinForm(request.POST)
            if form.is_valid():
                newJoin = form.save(commit=False)
                    #add condition as necessary
                newJoin.save()

                if not TeamCreation.objects.filter(team_name=newJoin.team_name).exists():
                    messages.error(request, f'Please try again, this team does not exist')
                    return redirect('dashboard')                    
                else:
                    #assign team
                    group_name=newJoin.team_name            
                    user = request.user
                    user.profile.team_num1=group_name
                    user.profile.save()
                    newJoin.save()
         
                    #redirect homepage
                    team_name = form.cleaned_data.get('team_name')
                    username = user.username
                    messages.success(request, f'Successfully joined {team_name}! Welcome aboard {username}!')
                    return redirect('dashboard')
        else:
            form=JoinForm()
    
        context={
                "form":form,
                "d_upload":d_upload,
                "d_access":d_access,
                "d_email":d_email,
                "g_daily":g_daily,
                "g_pref":g_pref,
                "g_goal":g_goal,
                "t_test":t_test,
                "t_imp":t_imp,
                }
    
        return render(request, "pages/dashboard.html", context)

@login_required
def upload(request):
    context={}
    if request.method=='POST':
        uploaded_file=request.FILES['document']


        
        #actual pdf reader - pypdf2
        pdfFileObj = uploaded_file.read() 
        pdfReader = PyPDF2.PdfFileReader(io.BytesIO(pdfFileObj))
        
        search_date_17 = "2017"
        search_date_18 = "2018"
        search_date_19 = "2019"
        search_date_20 = "2020"        
        search_date_21 = "2021"
        
        search_word_count_17 = 0
        search_word_count_18 = 0       
        search_word_count_19 = 0    
        search_word_count_20 = 0
        search_word_count_21 = 0
        
        for pageNum in range(1, pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            text = pageObj.extractText().encode('utf-8')
            search_text = text.lower().split()
            for word in search_text:
                
                if search_date_17 in word.decode("utf-8"):
                    search_word_count_17 += 1
                if search_date_18 in word.decode("utf-8"):
                    search_word_count_18 += 1
                if search_date_19 in word.decode("utf-8"):
                    search_word_count_19 += 1
                if search_date_20 in word.decode("utf-8"):
                    search_word_count_20 += 1
                if search_date_21 in word.decode("utf-8"):
                    search_word_count_21 += 1
        
        for pageNum in range(1, pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            text = pageObj.extractText().encode('utf-8')
            if (pageNum==5):
                strPage6=text
        
        
        #if GLOBAL SCORE is one digit
        if (strPage6[33:34]==b"%"):
            g_score=str[32:33]
            print("global score is")
            print(g_score)
            
        #if GLOBAL SCORE is two digits         
        else:
            g_score=strPage6[32:34]    
            print("global score is")
            print(g_score)
            
            #if WELLNESS is one digit
            if (strPage6[162:163]==b"%"):
                well_being=strPage6[161:162]             
                print("well-being is")     
                print(well_being)
                
            #if WELLNESS is two digits
            else:
                well_being=strPage6[161:163]            
                print("well-being is")     
                print(well_being)

                #if HAPPINESS is one digit:            
                if (strPage6[165:166]==b"%"):
                    happy=strPage6[164:165]
                    print("happiness is")
                    print(happy)
                
                #if HAPPINESS is two digits:
                else:
                    happy=strPage6[164:166]
                    print("happiness is")
                    print(happy)
                
                    #if OPTIMISM is one digit:
                    if (strPage6[168:169]==b"%"):
                        optimism=strPage6[167:168]
                        print("optimism is")
                        print(optimism)
                        
                    #if OPTIMISM is two digits:    
                    else:
                        optimism=strPage6[167:169]
                        print("optimism is")
                        print(optimism)                        
                        
                        #if SELF-ESTEEM is one digit:
                        if (strPage6[171:172]==b"%"):
                            s_esteem=strPage6[170:171]
                            print("self-esteem is")
                            print(s_esteem)
                            
                        #if SELF-ESTEEM IS two digits:
                        else:
                            s_esteem=strPage6[170:172]
                            print("self-esteem is")
                            print(s_esteem)
                            
                            #if SELF-CONTROL is one digit:
                            if (strPage6[324:325]==b"%"):
                                s_control=strPage6[323:324]
                                print("self-control is")
                                print(s_control)
                            
                            #if SELF-CONTROL is two digits:
                            else:
                                s_control=strPage6[323:325]
                                print("self-control is")
                                print(s_control)
                                
                                #if EMOTION REGULATION is one digit:
                                if (strPage6[327:328]==b"%"):
                                    e_regulation=strPage6[326:327]
                                    print("emotion reg is")
                                    print(e_regulation)
                                
                                #if EMOTION REGULATION IS two digits:
                                else:
                                    e_regulation=strPage6[326:328]
                                    print("emotion reg is")
                                    print(e_regulation)
                                    
                                    #if IMPULSE CONTROL is one digit:
                                    if (strPage6[330:331]==b"%"):
                                        imp_ctrl=strPage6[329:330]
                                        print("impulse ctrl is")
                                        print(imp_ctrl)

                                        #if STRESS MGT is one digit:
                                        if (strPage6[332:333]==b"%"):
                                            stress_mgt=strPage6[331:332]
                                            print("stress mgt is")
                                            print(stress_mgt)
                                            
                                        #if STRESS MGT is two digits:
                                        else:
                                            stress_mgt=strPage6[331:333]
                                            print("stress mgt is")
                                            print(stress_mgt)
                                            
                                            #if EMOTIONALITY is one digit:
                                            if (strPage6[491:492]==b"%"):
                                                emotionality=strPage6[490:491]
                                                print("emotionality is")
                                                print(emotionality)
                                                
                                            #if EMOTIONALITY is two digits:
                                            else:
                                                emotionality=strPage6[490:492]
                                                print("emotionality is")
                                                print(emotionality)                                                
                                            
                                                #if EMPATHY is one digits
                                                if (strPage6[494:495]==b"%"):
                                                    empathy=strPage6[493:494]
                                                    print("empathy is")
                                                    print(empathy)
                                                
                                                #if EMPATHY is two digits
                                                else:
                                                    empathy=strPage6[493:495]
                                                    print("empathy is")
                                                    print(empathy)
                                                
                                                    #if EMOTION PERCEPTION is one digit:
                                                    if (strPage6[497:498]==b"%"):
                                                        emotion_perc=strPage6[496:497]
                                                        print("emotion perception is")
                                                        print(emotion_perc)
                                                    
                                                    #if EMOTION PERCEPTION is two digits:
                                                    else:
                                                        emotion_perc=strPage6[496:498]
                                                        print("emotion perception is")
                                                        print(emotion_perc)
                                                        
                                                        #if EMOTION EXPRESSION is one digit
                                                        if (strPage6[500:501]==b"%"):
                                                            emotion_exp=strPage6[499:500]
                                                            print("emotion expression is")
                                                            print(emotion_exp)

                                                        #if EMOTION EXPRESSION is two digits:                                                        
                                                        else:
                                                            emotion_exp=strPage6[499:501]
                                                            print("emotion expression is")
                                                            print(emotion_exp)
                                                            
                                                            #if RELATIONSHIPS is one digit:
                                                            if (strPage6[503:504]==b"%"):
                                                                relation=strPage6[502:503]
                                                                print("relation is")
                                                                print(relation)

                                                            #if RELATIONSHIPS is two digits:
                                                            else:
                                                                relation=strPage6[502:504]
                                                                print("relation is")
                                                                print(relation)
                                                                
                                                                #if SOCIALIBILITY is one digit:
                                                                if (strPage6[652:653]==b"%"):
                                                                    socialibility=strPage6[651:652]
                                                                    print("socialibility is")
                                                                    print(socialibility)
                                                                
                                                                #if SOCIALIBILITY is two digits:
                                                                else:
                                                                    socialibility=strPage6[651:653]
                                                                    print("socialibility is")
                                                                    print(socialibility)
                                                                                                                                      
                                                                    #if EMOTION MGT is one digit:
                                                                    if (strPage6[655:656]==b"%"):
                                                                        emotion_mgt=strPage6[654:655]
                                                                        print("emotion mgt is")
                                                                        print(emotion_mgt)
                                                                    
                                                                    #if EMOTION MGT is two digits:
                                                                    else:
                                                                        emotion_mgt=strPage6[654:656]
                                                                        print("emotion mgt is")
                                                                        print(emotion_mgt)
                                                                    
                                                                        #if assertiveness is one digit:
                                                                        if (strPage6[658:659]==b"%"):
                                                                            assertive=strPage6[657:658]
                                                                            print("assertiveness is")
                                                                            print(assertive)
                                                                            
                                                                        #2 digits
                                                                        else:
                                                                            assertive=strPage6[657:659]
                                                                            print("assertiveness is")
                                                                            print(assertive)
                                                                            
                                                                            #if socialawareness is one digit
                                                                            if (strPage6[661:662]==b"%"):
                                                                                social_awa=strPage6[660:661]
                                                                                print("social awareness is")
                                                                                print(social_awa)
                                                                            else:
                                                                                social_awa=strPage6[660:662]
                                                                                print("social awareness is")
                                                                                print(social_awa)
                                                                                
                                                                                #if ADAPTIBILITY is one digit
                                                                                if (strPage6[790:791]==b"%"):
                                                                                    adaptability=strPage6[789:790]
                                                                                    print("adaptability is")
                                                                                    print(adaptability)
                                                                                #if ADAPTABILITY is two digits
                                                                                else:
                                                                                    adaptability=strPage6[789:791]
                                                                                    print("adaptability is")
                                                                                    print(adaptability)
                                                                                    
                                                                                    #if SELF-MOT is one digit
                                                                                    if (strPage6[793:794]==b"%"):
                                                                                        s_motivation=strPage6[792:793]
                                                                                        print("self-motivation is")
                                                                                        print(s_motivation)
                                                                                    else:
                                                                                        s_motivation=strPage6[792:794]
                                                                                        print("self-motivation is")
                                                                                        print(s_motivation)
                                                                                        
                                                                        
                                    #if IMPULSE CTRL is two digits:
                                    else:
                                        imp_ctrl=strPage6[329:331]
                                        print("impulse ctrl is - 2 digits")
                                        print(imp_ctrl)
                                        
        user = request.user                                       
        if search_word_count_17> max(search_word_count_18, search_word_count_19, search_word_count_20, search_word_count_21):
            #date is 2017
            user.profile.adaptability17=int(adaptability)
            user.profile.happiness17=int(happy)
            user.profile.optimism17=int(optimism)
            user.profile.sesteem17=int(s_esteem)
            user.profile.emotion_reg17=int(e_regulation)
            user.profile.impulse_ctrl17=int(imp_ctrl)
            user.profile.stress_mgt17=int(stress_mgt)
            user.profile.empathy17=int(empathy)
            user.profile.emotionperc17=int(emotion_perc)
            user.profile.emotion_exp17=int(emotion_exp)
            user.profile.relationship17=int(relation)
            user.profile.emotion_mgt17=int(emotion_mgt)
            user.profile.assertive17=int(assertive)
            user.profile.socialawa17=int(social_awa)
            user.profile.smotivation17=int(s_motivation)
            user.profile.wellbeing17=int(well_being)
            user.profile.scontrol17=int(s_control)
            user.profile.emotionality17=int(emotionality)
            user.profile.socialibility17=int(socialibility)          
            user.profile.save()
            
        if search_word_count_18> max(search_word_count_17, search_word_count_19, search_word_count_20, search_word_count_21):
            #date is 2018
            user.profile.adaptability18=int(adaptability)
            user.profile.happiness18=int(happy)
            user.profile.optimism18=int(optimism)
            user.profile.sesteem18=int(s_esteem)
            user.profile.emotion_reg18=int(e_regulation)
            user.profile.impulse_ctrl18=int(imp_ctrl)
            user.profile.stress_mgt18=int(stress_mgt)
            user.profile.empathy18=int(empathy)
            user.profile.emotionperc18=int(emotion_perc)
            user.profile.emotion_exp18=int(emotion_exp)
            user.profile.relationship18=int(relation)
            user.profile.emotion_mgt18=int(emotion_mgt)
            user.profile.assertive18=int(assertive)
            user.profile.socialawa18=int(social_awa)
            user.profile.smotivation18=int(s_motivation)
            user.profile.wellbeing18=int(well_being)
            user.profile.scontrol18=int(s_control)
            user.profile.emotionality18=int(emotionality)
            user.profile.socialibility18=int(socialibility)           
            user.profile.save()
            
        if search_word_count_19> max(search_word_count_18, search_word_count_17, search_word_count_20, search_word_count_21):
            #date is 2019
            user.profile.adaptability19=int(adaptability)
            user.profile.happiness19=int(happy)
            user.profile.optimism19=int(optimism)
            user.profile.sesteem19=int(s_esteem)
            user.profile.emotion_reg19=int(e_regulation)
            user.profile.impulse_ctrl19=int(imp_ctrl)
            user.profile.stress_mgt19=int(stress_mgt)
            user.profile.empathy19=int(empathy)
            user.profile.emotionperc19=int(emotion_perc)
            user.profile.emotion_exp19=int(emotion_exp)
            user.profile.relationship19=int(relation)
            user.profile.emotion_mgt19=int(emotion_mgt)
            user.profile.assertive19=int(assertive)
            user.profile.socialawa19=int(social_awa)
            user.profile.smotivation19=int(s_motivation)
            user.profile.wellbeing19=int(well_being)
            user.profile.scontrol19=int(s_control)
            user.profile.emotionality19=int(emotionality)
            user.profile.socialibility19=int(socialibility)            
            user.profile.save()
 
        if search_word_count_20> max(search_word_count_18, search_word_count_19, search_word_count_17, search_word_count_21):
            #date is 2020
            user.profile.adaptability20=int(adaptability)
            user.profile.happiness20=int(happy)
            user.profile.optimism20=int(optimism)
            user.profile.sesteem20=int(s_esteem)
            user.profile.emotion_reg20=int(e_regulation)
            user.profile.impulse_ctrl20=int(imp_ctrl)
            user.profile.stress_mgt20=int(stress_mgt)
            user.profile.empathy20=int(empathy)
            user.profile.emotionperc20=int(emotion_perc)
            user.profile.emotion_exp20=int(emotion_exp)
            user.profile.relationship20=int(relation)
            user.profile.emotion_mgt20=int(emotion_mgt)
            user.profile.assertive20=int(assertive)
            user.profile.socialawa20=int(social_awa)
            user.profile.smotivation20=int(s_motivation)
            user.profile.wellbeing20=int(well_being)
            user.profile.scontrol20=int(s_control)
            user.profile.emotionality20=int(emotionality)
            user.profile.socialibility20=int(socialibility)           
            user.profile.save()

        if search_word_count_21> max(search_word_count_18, search_word_count_19, search_word_count_20, search_word_count_17):
            #date is 2021
            user.profile.adaptability21=int(adaptability)
            user.profile.happiness21=int(happy)
            user.profile.optimism21=int(optimism)
            user.profile.sesteem21=int(s_esteem)
            user.profile.emotion_reg21=int(e_regulation)
            user.profile.impulse_ctrl21=int(imp_ctrl)
            user.profile.stress_mgt21=int(stress_mgt)
            user.profile.empathy21=int(empathy)
            user.profile.emotionperc21=int(emotion_perc)
            user.profile.emotion_exp21=int(emotion_exp)
            user.profile.relationship21=int(relation)
            user.profile.emotion_mgt21=int(emotion_mgt)
            user.profile.assertive21=int(assertive)
            user.profile.socialawa21=int(social_awa)
            user.profile.smotivation21=int(s_motivation)
            user.profile.wellbeing21=int(well_being)
            user.profile.scontrol21=int(s_control)
            user.profile.emotionality21=int(emotionality)
            user.profile.socialibility21=int(socialibility)
            user.profile.save()

        #prepare and save file  (content,url...)
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name,uploaded_file)
        context['url']=fs.url(name)
        
        #user can now access myGoals
        user.profile.completed_a_test=True

    return render(request,'pages/upload.html', context)

@login_required
def mydata(request):
#   *** TESTED and working
    user=request.user
    if (user.profile.team_num1==""):
        #   GROUP DATA HERE:
        print("no team assigned, hence no group data")
        
        #   PERSONAL DATA HERE:
        
    else:
        #   GROUP DATA HERE:
        members = Profile.objects.filter(team_num1=user.profile.team_num1)
#           '17
#               [...]        
#           '18
        globalscore17,globalscore18,globalscore19,globalscore20,globalscore21=[],[],[],[],[]
        belowavg17,belowavg18,belowavg19,belowavg20,belowavg21=0,0,0,0,0
        avg17,avg18,avg19,avg20,avg21=0,0,0,0,0
        aboveavg17,aboveavg18,aboveavg19,aboveavg20,aboveavg21=0,0,0,0,0
        year17=False
        year18=False
        year19=False
        year20=False
        year21=False
        counter=0
        teamname=user.profile.team_num1
        data_heatmap=[]
        data17,data18,data19,data20,data21=[],[],[],[],[]
        column_data17,column_data18,column_data19,column_data20,column_data21=[],[],[],[],[]
        stat118, stat218, stat318, stat418, stat518, stat618, stat718, stat818, stat918, stat1018, stat1118, stat1218, stat1318,stat1418, stat1518, stat1618, stat1718=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
        #prepare .csv file for later
        with open('mycsv.csv','w') as f:
            fieldnames=['User','Global Score','Happiness','Optimism','Self-Esteem','Emotional Regulation','Impulse Control','Empathy',
                        'Emotion Perception','Emotion Expression','Relationships','Emotion Management','Social Awareness',
                        'Adaptability','Self-Motivation','Well-Being','Self-Control','Emotionality','Socialibility']
            thewriter=csv.DictWriter(f,fieldnames=fieldnames)
            thewriter.writeheader()
            for user in members:
                if (user.adaptability18==0):
                    print("")
                else:
                    counter+=1
                    userxname="user"+str(counter)
                    z1results=(user.happiness18)
                    z2results=(user.optimism18)
                    z3results=(user.sesteem18)
                    z4results=(user.emotion_reg18)
                    z5results=(user.impulse_ctrl18)
                    z6results=(user.empathy18)
                    z7results=(user.emotionperc18)
                    z8results=(user.emotion_exp18)
                    z9results=(user.relationship18)
                    z10results=(user.emotion_mgt18)
                    z11results=(user.socialawa18)
                    z12results=(user.adaptability18)
                    z13results=(user.smotivation18)
                    z14results=(user.wellbeing18)
                    z15results=(user.scontrol18)
                    z16results=(user.emotionality18)
                    z17results=(user.socialibility18)
                    
                    results=[z1results,z2results,z3results,z4results,z5results,z6results,z7results,z8results,
                                   z9results,z10results,z11results,z12results,z13results,z14results,z15results,z16results,z17results]
                    data18.append(results)
                    #global score
                    resultsGS=round(mean(results))       
                    
                    globalscore18.append(resultsGS)
                    stat118.append(z1results)
                    stat218.append(z2results)
                    stat318.append(z3results)
                    stat418.append(z4results)
                    stat518.append(z5results)
                    stat618.append(z6results)
                    stat718.append(z7results)
                    stat818.append(z8results)
                    stat918.append(z9results)
                    stat1018.append(z10results)
                    stat1118.append(z11results)
                    stat1218.append(z12results)
                    stat1318.append(z13results)                    
                    stat1418.append(z14results)
                    stat1518.append(z15results)
                    stat1618.append(z16results)
                    stat1718.append(z17results)
                    
                    # prepare heatmap format
                    record=[userxname,resultsGS, z1results,z2results,z3results,z4results,z5results,z6results,z7results,z8results,
                            z9results,z10results,z11results,z12results,z13results,z14results,z15results,z16results,z17results]
                    data_heatmap.append(record)                                

                    #count GS distribution (for histogram)
                    if (resultsGS<29):
                        belowavg18+=1
                    if ( (resultsGS>29) and (resultsGS<70) ):
                        avg18+=1
                    if (resultsGS>70):
                        aboveavg18+=1

                    #prepare csv file
                    thewriter.writerow(
                            {
                            'Global Score':resultsGS,
                            'Happiness':z1results,
                            'Optimism':z2results,
                            'Self-Esteem':z3results,
                            'Emotional Regulation':z4results,
                            'Impulse Control':z5results,
                            'Empathy':z6results,
                            'Emotion Perception':z7results,
                            'Emotion Expression':z8results,
                            'Relationships':z9results,
                            'Emotion Management':z10results,
                            'Social Awareness':z11results,
                            'Adaptability':z12results,
                            'Self-Motivation':z13results,
                            'Well-Being':z14results,
                            'Self-Control':z15results,
                            'Emotionality':z16results,
                            'Socialibility':z17results})
                    #there is '18 data available, ticker ON
                    year18=True
#       '19
#       [...]
#       '20
#       [...]
#       '21
#       [...]
        column_data18=[mean(globalscore18),mean(stat118),mean(stat218),mean(stat318),mean(stat418),mean(stat518),mean(stat618),mean(stat718),mean(stat818),mean(stat918),
                       mean(stat1018),mean(stat1118),mean(stat1218),mean(stat1318),mean(stat1418),mean(stat1518),mean(stat1618),mean(stat1718)]
#   prepare dataset - general use
        if ( (year17==True) and (year18==False) and (year19==False) and (year20==False) and (year21==False)):
            teams=teamname
            years = ['2017']
            data = {'team' : teams,
                    '2017'   : column_data17,}
            average = mean(zip(data['2017']), ())

        if ( (year17==True) and (year18==True) and (year19==False) and (year20==False) and (year21==False) ):
            teams=teamname
            years = ['2017','2018']
            data = {'team' : teams,
                    '2017'   : column_data17,
                    '2018'   : column_data18,}
            average = mean(zip(data['2015'], data['2016'], data['2017']), ())

        if ( (year17==True) and (year18==True) and (year19==True) and (year20==False) and (year21==False)):
            teams=teamname
            years = ['2017','2018','2019']
            data = {'team' : teams,
                    '2017'   : column_data17,
                    '2018'   : column_data18,
                    '2019'   : column_data19,}
            average = mean(zip(data['2015'], data['2016'], data['2017']), ())

        if ( (year17==True) and (year18==True) and (year19==True) and (year20==True) and (year21==False)):
            years = ['2017','2018','2019','2020']
            data = {'team' : teams,
                    '2017'   : column_data17,
                    '2018'   : column_data18,
                    '2019'   : column_data19,
                    '2020'   : column_data20,}
            average = mean(zip(data['2015'], data['2016'], data['2017']), ())

        if ( (year17==True) and (year18==True) and (year19==True) and (year20==True) and (year21==True)):
            teams=teamname
            years = ['2017','2018','2019','2020','2021']
            data = {'team' : teams,
                    '2017'   : column_data17,
                    '2018'   : column_data18,
                    '2019'   : column_data19,
                    '2020'   : column_data20,
                    '2021'   : column_data21,}
        if ( (year17==False) and (year18==True) and (year19==True) and (year20==True) and (year21==True)):
            years = ['2018','2019','2020','2021']
            teams=teamname
            data = {'team' : teams,
                    '2018'   : column_data18,
                    '2019'   : column_data19,
                    '2020'   : column_data20,
                    '2021'   : column_data21,}
        if ( (year17==False) and (year18==False) and (year19==True) and (year20==True) and (year21==True)):
            teams=teamname
            years = ['2019','2020','2021']
            data = {'team' : teams,
                    '2019'   : column_data19,
                    '2020'   : column_data20,
                    '2021'   : column_data21,}            
        if ( (year17==False) and (year18==False) and (year19==False) and (year20==True) and (year21==True)):
            teams=teamname
            years = ['2020','2021']
            data = {'team' : teams,
                    '2020'   : column_data20,
                    '2021'   : column_data21,}
        if ( (year17==False) and (year18==False) and (year19==False) and (year20==False) and (year21==True)):
            teams=teamname
            years = ['2021']
            data = {'team' : teams,
                    '2021'   : column_data21,}
        if ( (year17==False) and (year18==True) and (year19==False) and (year20==False) and (year21==False)):
            distribution = ['Below Average', 'Average', 'Above Average']
            years = ['2018']
            
            data = {'distribution' : distribution,
                    '2018'   : [belowavg18, avg18, aboveavg18],}

            
            
            # this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
            x = [ ('Below Average', '2018'),('Average','2018'),('Above Average','2018') ]
            x2 = [ ('2018','Below Average'),('2018','Average'),('2018','Above Average') ]
        if ( (year17==False) and (year18==False) and (year19==True) and (year20==False) and (year21==False)):
            teams=teamname
            years = ['2019']
            data = {'team' : teams,
                    '2019'   : column_data19,}
        if ( (year17==False) and (year18==False) and (year19==False) and (year20==True) and (year21==False)):
            teams=teamname
            years = ['2020']
            data = {'team' : teams,
                    '2020'   : column_data20,}


# *** TESTED and working
# *** H E A T M A P -----------------------------------------------------------------------------------------------------------------------------------------
    data_heatmap = pd.DataFrame(data_heatmap, columns = ['User','Global Score','Happiness','Optimism','Self-Esteem','Emotional Regulation','Impulse Control','Empathy',
                                                         'Emotion Perception','Emotion Expression','Relationships','Emotion Management','Social Awareness',
                                                         'Adaptability','Self-Motivation','Well-Being','Self-Control','Emotionality','Socialibility'])
    data_heatmap.User = data_heatmap.User.astype(str)
    data_heatmap = data_heatmap.set_index('User')
    data_heatmap.columns.name = 'Month'
    
    # reshape to 1D array or rates with a month and year for each row.
    df_heatmap = pd.DataFrame(data_heatmap.stack(), columns=['rate']).reset_index()
    source_heatmap = ColumnDataSource(df_heatmap)
    # this is the colormap from the original NYTimes plot
    colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
    mapper = LinearColorMapper(palette=colors, low=df_heatmap.rate.min(), high=df_heatmap.rate.max())
    plt2 = figure(plot_width=900, plot_height=400, title=None,
               x_range=list(data_heatmap.index), y_range=list(reversed(data_heatmap.columns)),
                x_axis_location='above', toolbar_location=None)

    hover = HoverTool(
    tooltips = """
        <div>

            <div style="color:#2b2c34; font-family: 'Space Mono', monospace;">
                <span>@rate</span><span>%</span>
            </div>

        </div>
    """

    )
    tools = [ResetTool(), SaveTool(),  PanTool(), ZoomInTool(), BoxSelectTool(), BoxZoomTool(), hover, ZoomOutTool()]
    plt2.tools= tools
    toolBarBox = ToolbarBox()
    toolBarBox.toolbar = Toolbar(tools=tools)
    toolBarBox.toolbar_location = "right"
    toolBarBox.toolbar.logo = None
    
    #add manually the custom-made toolbar
    
    plt2.rect(x='User', y="Month", width=1, height=1, source=source_heatmap,
           line_color=None, fill_color=transform('rate', mapper))
    
    color_bar = ColorBar(color_mapper=mapper, location=(0, 0),
                         ticker=BasicTicker(desired_num_ticks=len(colors)),
                         formatter=PrintfTickFormatter(format="   %d%%"))
    plt2.add_layout(color_bar, 'right')
    
    plt2.axis.axis_line_color = None
    plt2.axis.major_tick_line_color = None
    plt2.axis.major_label_text_font_size = "5pt"
    plt2.axis.major_label_standoff = 0
    plt2.xaxis.major_label_orientation = 1.0
    #hide 'user 1' on xaxis
    plt2.xaxis.visible = False
   
    
    toexport_graph=(row(plt2,toolBarBox)) 
    
    script1, div1 = components(toexport_graph)
# *** H E A T M A P -----------------------------------------------------------------------------------------------------------------------------------------
 
# HISTOGRAM ---------------------------------------
    counts = sum(zip(data['2018']), ()) # like an hstack
    source = ColumnDataSource(data=dict(x=x, counts=counts))
    hover = HoverTool(
        tooltips=[
            ( 'Count','@counts{0}'),
        ],
    )
    tools = [ResetTool(), SaveTool(),  PanTool(), ZoomInTool(), BoxSelectTool(), BoxZoomTool(), hover, ZoomOutTool()]
    plthisto = figure(x_range=FactorRange(*x), plot_height=400, plot_width=900, title="Distribution Count by Results",
               toolbar_location=None, tools=tools, y_range=(0,counter))
    toolBarBox = ToolbarBox()
    toolBarBox.toolbar = Toolbar(tools=tools)
    toolBarBox.toolbar_location = "right"
    toolBarBox.toolbar.logo = None   
    plthisto.vbar(x='x', top='counts', width=0.9, source=source)
    
    plthisto.y_range.start = 0
    plthisto.x_range.range_padding = 0.1
    plthisto.xaxis.major_label_orientation = 1
    plthisto.xgrid.grid_line_color = None
    plthisto.ygrid.grid_line_color = None

# HISTOGRAM ---------------------------------------  
    histo_complete=(row(plthisto,toolBarBox)) 

    div4,script4=components(histo_complete)
    
# LINE CHART ---------------------------------------
    counts = sum(zip(data['2018']), ()) # like an hstack
    source = ColumnDataSource(data=dict(x=x2, counts=counts))
    hover = HoverTool(
        tooltips=[
            ( 'Count','@counts{0}'),
        ],
    )
    tools = [ResetTool(), SaveTool(),  PanTool(), ZoomInTool(), BoxSelectTool(), BoxZoomTool(), hover, ZoomOutTool()]
    pltline = figure(x_range=FactorRange(*x), plot_height=400, plot_width=900, title="Distribution Count by Year",
               toolbar_location=None, tools=tools, y_range=(0,counter))
    toolBarBox = ToolbarBox()
    toolBarBox.toolbar = Toolbar(tools=tools)
    toolBarBox.toolbar_location = "right"
    toolBarBox.toolbar.logo = None   
    pltline.vbar(x='x', top='counts', width=0.9, source=source)
    
    pltline.y_range.start = 0
    pltline.x_range.range_padding = 0.1
    pltline.xaxis.major_label_orientation = 1
    pltline.xgrid.grid_line_color = None
    pltline.ygrid.grid_line_color = None

# LINE CHART  ---------------------------------------  
    line_complete=(row(pltline,toolBarBox)) 

    div5,script5=components(line_complete)
#     *** Excel File *** ------------------------------------------------------------------------------------------------------------------------------------
#    df = pd.read_csv('salary_data.csv')
#    
#    source = ColumnDataSource(data=dict())
#    
#    def update():
#        current = df[(df['salary'] >= slider.value[0]) & (df['salary'] <= slider.value[1])].dropna()
#        source.data = {
#            'name'             : current.name,
#            'salary'           : current.salary,
#            'years_experience' : current.years_experience,
#        }
#    
#    slider = RangeSlider(title="Max Salary", start=10000, end=110000, value=(10000, 50000), step=1000, format="0,0")
#    slider.on_change('value', lambda attr, old, new: update())
#    
#    button = Button(label="Download", button_type="success")
#    button.js_on_click(CustomJS(args=dict(source=source),
#                                code=open(join(dirname(__file__), "download.js")).read()))
#    
#    columns = [
#        TableColumn(field="name", title="Employee Name"),
#        TableColumn(field="salary", title="Income", formatter=NumberFormatter(format="$0,0.00")),
#        TableColumn(field="years_experience", title="Experience (years)")
#    ]
#    
#    data_table = DataTable(source=source, columns=columns, width=800)
#    
#    controls = column(slider, button)
#    
#    curdoc().add_root(row(controls, data_table))
#    curdoc().title = "Export CSV"
#    
#    update()
#    script2, div2=components(curdoc()) 
# *** Excel File ----------------------------------------------------------------------------------------------------------------------------------------------

# *** H E X M A P  ----------------------------------------------------------------------------------------------------------------------------------------------

#   global score - (by default)
    x_toconvert = globalscore18
#   happiness - (by default)
    y_toconvert = globalscore18
#   + selfesteem - (option)   
    x = np.asarray(x_toconvert, dtype=np.float32)
    y = np.asarray(y_toconvert, dtype=np.float32)
    
    bins = hexbin(x, y, 4)
    
    p = figure(title="", tools="wheel_zoom,pan,reset, box_zoom, lasso_select, pan, save, zoom_in, zoom_out",
               match_aspect=True, background_fill_color='#440154', plot_width=900, plot_height=400)
    p.grid.visible = False
    p.toolbar.logo = None
    
    p.hex_tile(q="q", r="r", size=0.1, line_color=None, source=bins, fill_color=linear_cmap('counts', 'Viridis256', 0, max(bins.counts)))

    script2,div2=components(p)
# *** H E X M A P  ----------------------------------------------------------------------------------------------------------------------------------------------
# *** H E X M A P  w/ tooltips -----------------------------------------------------------------------------------------------------------------------------------

    x_toconvert = globalscore18
    y_toconvert = globalscore18
    
    x = np.asarray(x_toconvert, dtype=np.float32)
    y = np.asarray(y_toconvert, dtype=np.float32)
    
    p1 = figure(title="", match_aspect=True,
               tools="wheel_zoom,reset, box_zoom, lasso_select, pan, save, zoom_in, zoom_out",
               background_fill_color='#440154', plot_width=900, plot_height=400)
    p1.grid.visible = False
    
    p1.xaxis.axis_label = "Team"
    p1.yaxis.axis_label = "Organization"
    
    p1.width=600
    p1.height=600
    
    
    r, bins = p1.hexbin(x, y, size=5, hover_color="pink", hover_alpha=0.8)
    
    p1.circle(x, y, color="white", size=1)
    
    p1.add_tools(HoverTool(
        tooltips=[("count", "@c"), ("(Team, Org)", "(@q, @r)")],
        mode="mouse", point_policy="follow_mouse", renderers=[r]
    ))
    
    p1.toolbar.logo = None
    script3,div3=components(p1)
# *** H E X M A P  w/ tooltips -----------------------------------------------------------------------------------------------------------------------------------

    context={
            'script1':script1,'div1':div1,
            'script2':script2,'div2':div2,
            'script3':script3,'div3':div3,
            'script4':script4,'div4':div4,
            'script5':script5,'div5':div5,

            }
    return render_to_response('pages/mydata.html', context)

@login_required
def mygoals(request):
    if request.method == 'POST':
        form = PreferencesForm(request.POST)
        if form.is_valid():
            preferences = form.save(commit=False)
            gender=preferences.gender
            experience=preferences.experience
            areawork=preferences.areawork
            aspirations=preferences.aspirations
            user = request.user
            user.profile.gender=gender
            user.profile.experience=experience
            user.profile.areawork=areawork
            user.profile.aspirations=aspirations
            user.profile.save()
            return redirect('dashboard')
    else:
        form = PreferencesForm()
    return render(request,'pages/goals.html', {'form':form})
