import requests as rq
import obspython as obs
from config import *


source_name = ""
text_streamer = ""
text_followers = ""
streamer_id = ""
data = {}


def script_description():
    return "Set credits to a specific Text Source, when switching to a given Scene. Credits are a list of followers."


def script_properties():
    props = obs.obs_properties_create()
    sources = obs.obs_enum_sources()
    properties = obs.obs_properties_add_list(props, "source", "Text Source",
                                    obs.OBS_COMBO_TYPE_EDITABLE,
                                    obs.OBS_COMBO_FORMAT_STRING)
    
    obs.obs_properties_add_text(props, "streamer_id", "Streamer ID", obs.OBS_TEXT_DEFAULT)
    
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(properties, name, name)

        obs.source_list_release(sources)

    return props


def script_load(settings):
    obs.obs_frontend_add_event_callback(handle_event)


def script_update(settings):
    global source_name
    global streamer_id

    source_name = obs.obs_data_get_string(settings, "source")
    streamer_id = obs.obs_data_get_string(settings, "streamer_id")


def handle_event(event):
    if event == obs.OBS_FRONTEND_EVENT_SCENE_CHANGED:
        handle_scene_change()


def handle_scene_change():
    global data

    scene = obs.obs_frontend_get_current_scene()
    scene_name = obs.obs_source_get_name(scene)

    if scene_name == "Fin":
        fetch_followers()
        print(data)
        if len(data) > 0:
            update_text()
            fill_text_source()
        else:
            print("This streamer has no followers.")

    obs.obs_source_release(scene)


def fetch_followers(): 
    global data

    header = {"Client-ID": client_id, "Authorization": f"Bearer {auth_token}"}
    response = rq.get(f"https://api.twitch.tv/helix/users/follows?to_id={streamer_id}&first=100", headers = header)
    data = response.json()['data']


def update_text():
    global text_streamer
    global text_followers

    text_streamer = f"{data[0]['to_name']}\n"

    for r in reversed(data):
        text_followers += f"{r['from_name']}\n"


def fill_text_source():
    global source_name
    global text_streamer
    global text_followers

    source = obs.obs_get_source_by_name(source_name)
    text_thanks = "Merci à tous\nd'avoir suivi !\n♥ ♥ ♥"
    text = f"\n\n\n\n\n\n\n\n\n\nStreamer\n-\n{text_streamer}\n\nFollowers\n-\n{text_followers}\n\n\n{text_thanks}"

    if source is not None:
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", text)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)
    
    text_followers = ""
