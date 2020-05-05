from django.shortcuts import render, render_to_response
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.transform import dodge, factor_cmap
from bokeh.models import Range1d, ColumnDataSource, BasicTicker, ColorBar,LinearColorMapper, PrintfTickFormatter, SaveTool, PanTool, ResetTool, ZoomInTool, BoxSelectTool, BoxZoomTool, HoverTool, RangeTool, ZoomOutTool
from bokeh.models.tools import Toolbar,  ToolbarBox
from PIL import ImageGrab
import pandas as pd
from bokeh.transform import transform
from bokeh.layouts import column, row
from bokeh.plotting import reset_output
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from .models import Post
# Create your views here.
#
def homepage(request):
   
        
    
    
    
        script=None
        div=None
        #store components
        
        #return to django homepage with components sent as arguments
        return render_to_response('pages/basic.html',{'script':script,'div':div})


def about(request):
    
    script=None
    div=None
    
    
    return render_to_response('pages/about.html',{'script':script,'div':div})

def contact(request):
    
    script=None
    div=None
    
    
    return render_to_response('pages/contact.html',{'script':script,'div':div})

def howitworks(request):
    
    script=None
    div=None
    
    
    return render_to_response('pages/howitworks.html',{'script':script,'div':div})

def storytelling(request):
 
    text = "hello world"  
    
    
    
    return render_to_response('pages/dashboard.html',{'text':text})

def dashboard(request):
    
    script=None
    div=None
    
    
    return render_to_response('pages/storytelling.html',{'script':script,'div':div})



