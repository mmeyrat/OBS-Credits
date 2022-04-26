import requests as rq
import obspython as obs
from config import *


source_name = ""
text = ""
streamer_id = "433976821"
data = {}


def script_description():
    return "Fill a text source with follower list."


def script_properties():
    props = obs.obs_properties_create()
    sources = obs.obs_enum_sources()
    p = obs.obs_properties_add_list(props, "source", "Text Source",
                                    obs.OBS_COMBO_TYPE_EDITABLE,
                                    obs.OBS_COMBO_FORMAT_STRING)
    
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)

    return props


def script_update(settings):
    global source_name
    
    source_name = obs.obs_data_get_string(settings, "source")


def fill_text_object():
    global source_name
    global text
    
    source = obs.obs_get_source_by_name(source_name)
    
    if source is not None:
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", text)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)


def update_text():
    global text

    for r in data:
        text += f"{r['from_name']}\n"


def script_load(settings):
    obs.obs_frontend_add_event_callback(handle_event)


def handle_event(event):
    if event == obs.OBS_FRONTEND_EVENT_SCENE_CHANGED:
        handle_scene_change()


def handle_scene_change():
    scene = obs.obs_frontend_get_current_scene()
    scene_name = obs.obs_source_get_name(scene)

    if scene_name == "Fin":
        fetch_followers()
        update_text()
        fill_text_object()

    obs.obs_source_release(scene)


def fetch_followers(): 
    global data

    header = {"Client-ID": client_id, "Authorization": f"Bearer {auth_token}"}
    response = rq.get(f"https://api.twitch.tv/helix/users/follows?to_id={streamer_id}", headers = header)
    data = response.json()["data"]

