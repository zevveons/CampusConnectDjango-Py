"""
Imports common Django tools: HttpResponse, render_to_response, RequestContext, Paginator, Http404, etc.
Uses models from cdi.home.models like Club, Event, and College.
This Django views module manages the display and filtering of clubs, events, and colleges on a website,
 allowing users to browse all items, view details, or filter them by popularity, type, region, or associated campus.
It uses Django's Paginator to paginate results (3 per page) and renders them using templates like clubs_all.html or event_detail.html.
It includes error handling for invalid IDs or empty query results via Http404. However, 
the code uses deprecated methods like render_to_response with RequestContext, and has several issues such as missing variables 
(offset_dict, type_dict) in regional filtering, which may cause some views to fail or behave unexpectedly.


"""

from django.http import HttpResponse

from django.shortcuts import render_to_response

from django.template import RequestContext

from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage

from django.core.exceptions import ObjectDoesNotExist

from django.http import Http404


from cdi.home.models import *


def clubs_all(request):

    club_list = Club.objects.all().order_by('?')

    paginator = Paginator(club_list, 3)


    page = request.GET.get('page')

    try:

        clubs = paginator.page(page)

    except PageNotAnInteger:

        clubs = paginator.page(1)

    except EmptyPage:

        clubs = paginator.page(paginator.num_pages)

    return render_to_response('home/clubs/clubs_all.html', {'club_list': clubs}, context_instance=RequestContext(request))


def clubs_popular(request):

    club_list = Club.objects.all().order_by('-popularity', 'name')[:10]

    paginator = Paginator(club_list, 3)


    page = request.GET.get('page')

    try:

        clubs = paginator.page(page)

    except PageNotAnInteger:

        clubs = paginator.page(1)

    except EmptyPage:

        clubs = paginator.page(paginator.num_pages)

    return render_to_response('home/clubs/clubs_all.html', {'club_list': clubs}, context_instance=RequestContext(request))


def clubs_campus(request, offset=1):

    try:

        clubs=Club.objects.filter(college__id__exact=int(offset))

    except (ValueError, ObjectDoesNotExist):

        raise Http404()

    if  clubs.count() == 0:

        raise Http404()

    cname = clubs[0].college.name

    return render_to_response('home/clubs/clubs_campus.html', {'cname': cname, 'club_list': clubs }, context_instance = RequestContext(request))


def clubs_region(request, offset=1):

    offset = int(offset)

    region_dict = {

            1: 'North',

            2: 'East',

            3: 'West',

            4: 'Central',

            5: 'South',

            }

    North = []

    East = []

    West = []

    Central = []

    South = []

    try:

        clubs=Club.objects.filter(club_type__exact=(type_dict[offset]))  #todo: WHERE and OR KEYWORD of SQL is needed. SEE how to make there kind of queries

    except (ValueError, ObjectDoesNotExist):

        raise Http404()

    if  clubs.count() == 0:

        raise Http404()

    cregion = region_dict[offset_dict]

    return render_to_response('home/clubs/clubs_type.html', {'cregion':cregion, 'club_list': clubs }, context_instance = RequestContext(request))


def clubs_types(request, offset=1):

    offset = int(offset)

    type_dict = {

            1: 'Engineering/Technology',

            2:'Applied Sciences',

            3: 'Social/NGO',

            4: 'Drama/Arts/Literature',

            5: 'Music/Bands',

            6: 'Management/Finance',

            7: 'Others',

            }

    MEMBERSHIP_CHOICE = (

        ('Open to anyone', 'Open to anyone'),

        ('Some Criteria', 'Some Criteria'),

        ('Through Apply and Selection', 'Through Apply and Selection'),

        ('Closed', 'Closed'),

            )

    try:

        clubs=Club.objects.filter(club_type__exact=(type_dict[offset]))

    except (ValueError, ObjectDoesNotExist):

        raise Http404()

    if  clubs.count() == 0:

        raise Http404()

    ctype = clubs[0].club_type

    return render_to_response('home/clubs/clubs_type.html', {'ctype':ctype, 'club_list': clubs }, context_instance = RequestContext(request))


def clubs_detail(request, offset=1):

    try:

        club = Club.objects.get(id=int(offset))

    except (ValueError, ObjectDoesNotExist):

        raise Http404()

    return render_to_response('home/clubs/club_detail.html', {'club': club }, context_instance = RequestContext(request))


##         EVENTS           ##


def events_all(request):

    event_list = Event.objects.all().order_by('start_date')

    paginator = Paginator(event_list, 3)


    page = request.GET.get('page')

    try:

        events = paginator.page(page)

    except PageNotAnInteger:

        events = paginator.page(1)

    except EmptyPage:

        events = paginator.page(paginator.num_pages)

    return render_to_response('home/events/events_all.html', {'event_list': events}, context_instance=RequestContext(request))


def events_popular(request):

    event_list = Event.objects.all().order_by('-popularity', 'name')[:10]

    paginator = Paginator(event_list, 3)


    page = request.GET.get('page')

    try:

        events = paginator.page(page)

    except PageNotAnInteger:

        events = paginator.page(1)

    except EmptyPage:

        events = paginator.page(paginator.num_pages)

    return render_to_response('home/events/events_all.html', {'event_list': events}, context_instance=RequestContext(request))


def events_campus(request, offset=1):

    try:

        events=Event.objects.filter(host__id__exact=int(offset))

    except (ValueError, ObjectDoesNotExist):

        raise Http404()

    if  events.count() == 0:

        raise Http404()

    cname = events[0].host.name

    return render_to_response('home/events/events_campus.html', {'cname': cname, 'event_list': events }, context_instance = RequestContext(request))


def events_region(request, offset=1):

    offset = int(offset)

    region_dict = {

            1: 'North',

            2: 'East',

            3: 'West',

            4: 'Central',

            5: 'South',

            }

    North = []

    East = []

    West = []

    Central = []

    South = []

    try:

        events=Event.objects.filter(event_type__exact=(type_dict[offset]))

    except (ValueError, ObjectDoesNotExist):

        raise Http404()

    if  events.count() == 0:

        raise Http404()

    eregion = type_dict[offset]

    return render_to_response('home/events/events_type.html', {'eregion':eregion, 'event_list': events }, context_instance = RequestContext(request))


def events_types(request, offset=1):

    offset = int(offset)

    type_dict = {

            1: 'Academics',

            2:'Seminar/Workshop',

            3: 'Party',

            4: 'Festival',

            5: 'Conference',

            6: 'Competition',

            7: 'Other',

            }

    try:

        events=Event.objects.filter(event_type__exact=(type_dict[offset]))

    except (ValueError, ObjectDoesNotExist):

        raise Http404()

    if  events.count() == 0:

        raise Http404()

    etype = events[0].event_type

    return render_to_response('home/events/events_type.html', {'etype':etype, 'event_list': events }, context_instance = RequestContext(request))


def events_detail(request, offset=1):

    try:

        event = Event.objects.get(id=int(offset))

    except (ValueError, ObjectDoesNotExist):

        raise Http404()

    return render_to_response('home/events/event_detail.html', {'event': event }, context_instance = RequestContext(request))


##         COLLEGES           ##


def colleges_all(request):

    college_list = College.objects.all().order_by('name')

    paginator = Paginator(college_list, 3)


    page = request.GET.get('page')

    try:

        colleges = paginator.page(page)

    except PageNotAnInteger:

        colleges = paginator.page(1)

    except EmptyPage:

        colleges = paginator.page(paginator.num_pages)

    return render_to_response('home/colleges/colleges_all.html', {'college_list': colleges}, context_instance=RequestContext(request))


def colleges_popular(request):

    college_list = College.objects.all().order_by('-rating', 'name')[:10]

    paginator = Paginator(college_list, 3)


    page = request.GET.get('page')

    try:

        colleges = paginator.page(page)

    except PageNotAnInteger:

        colleges = paginator.page(1)

    except EmptyPage:

        colleges = paginator.page(paginator.num_pages)

    return render_to_response('home/colleges/colleges_popular.html', {'college_list': colleges}, context_instance=RequestContext(request))


def colleges_region(request, offset=1):

    offset = int(offset)

    region_dict = {

            1: 'North',

            2: 'East',

            3: 'West',

            4: 'Central',

            5: 'South',

            }

    North = []

    East = []

    West = []

    Central = []

    South = []

    try:

        colleges=College.objects.filter(college_type__exact=(type_dict[offset]))

    except (ValueError, ObjectDoesNotExist):

        raise Http404()

    if  colleges.count() == 0:

        raise Http404()

    eregion = type_dict[offset]

    return render_to_response('home/colleges/colleges_type.html', {'eregion':eregion, 'college_list': colleges }, context_instance = RequestContext(request))


def colleges_types(request, offset=1):

    offset = int(offset)

    type_dict = {

            1: 'Arts/Commerce/Science',

            2: 'Engineering',

            3: 'Management',

            4: 'Law',

            5: 'Medical/Dental',

            6: 'Others',

            }

    try:

        colleges=College.objects.filter(college_type__exact=(type_dict[offset]))

    except (ValueError, ObjectDoesNotExist):

        raise Http404()

    if  colleges.count() == 0:

        raise Http404()

    cotype = colleges[0].college_type

    return render_to_response('home/colleges/colleges_type.html', {'cotype':cotype, 'college_list': colleges }, context_instance = RequestContext(request))


def colleges_detail(request, offset=1):

    try:

        college = College.objects.get(id=int(offset))

    except (ValueError, ObjectDoesNotExist):

        raise Http404()

    return render_to_response('home/colleges/college_detail.html', {'college': college }, context_instance = RequestContext(request))
