from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect


from ..models import InputData as InputData_model
from ..models import session

from ..models import *



def input_get_redirect_url(input_element, session):
    return input_element.redirect.get_absolute_url(session)

def input_generate_context(input_element, session):
    language = session.language
    redirect_url = input_get_redirect_url(input_element, session)


    voice_label = input_element.voice_label.get_voice_fragment_url(language)
    final_voice_label = input_element.final_voice_label.get_voice_fragment_url(language)

    context = { 'InputData': input_element,
               'redirect_url': redirect_url,
               'voice_label' : voice_label,
               'final_voice_label' : final_voice_label,
               }

    return context


def InputData(request, element_id, session_id):
    input_element = get_object_or_404(InputData_model, pk=element_id)
    voice_service = input_element.service
    session = lookup_or_create_session(voice_service, session_id)


    if request.method == "POST":
        session = get_object_or_404(CallSession, pk=session_id)

        value = 'DTMF_input'

        result = UserInput()

        result.input_value = request.POST.get('input_value')
        result.session = session
        result.category = input_element.input_category 

        result.save()

       
        return redirect(request.POST['redirect'])
        
                                     
    session.record_step(input_element)
    context = input_generate_context(input_element, session)

    context['url'] = request.get_full_path(False)

    return render(request, 'input.xml', context, content_type='text/xml')