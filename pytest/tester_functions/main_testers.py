from tester_functions.bg_listener_testers import helper_test_bg_listener_on, helper_test_bg_listener_off
from tester_functions.overlay_view_testers import helper_test_overlay_breakout_key_on, helper_test_overlay_breakout_key_off, helper_test_overlay_unicode_shortcut
from tester_functions.cp_view_testers import helper_test_control_panel_key, helper_test_close_control_panel
from tester_functions.latex_window_testers import helper_test_latex_output_enter
from tester_functions.navbar_component_testers import helper_test_navbar
from tester_functions.unicode_window_testers import helper_test_unicode_search_menu, helper_test_unicode_search_function,helper_test_unicode_copy_paste

def bg_listener_tester(test_env, subtests):
    
    helper_test_bg_listener_on(test_env, subtests)
    
    helper_test_bg_listener_off(test_env, subtests)

def overlay_tester(test_env, subtests):

    helper_test_bg_listener_on(test_env, subtests)

    helper_test_overlay_unicode_shortcut(test_env, subtests)

    helper_test_bg_listener_off(test_env, subtests)

def latex_tester(test_env, subtests):
    
    helper_test_bg_listener_on(test_env, subtests)

    helper_test_control_panel_key(test_env, subtests)

    helper_test_latex_output_enter(test_env, subtests)
    
    helper_test_bg_listener_off(test_env, subtests)

def navbar_tester(test_env, subtests):
    
    helper_test_bg_listener_on(test_env, subtests)

    helper_test_control_panel_key(test_env, subtests)

    helper_test_navbar(test_env, subtests)
    
    helper_test_bg_listener_off(test_env, subtests)

def unicode_tester(test_env, subtests):

    helper_test_bg_listener_on(test_env, subtests)

    helper_test_control_panel_key(test_env, subtests)

    helper_test_unicode_search_menu(test_env, subtests)

    helper_test_unicode_search_function(subtests)

    helper_test_unicode_copy_paste(subtests)

    helper_test_close_control_panel(test_env)

    helper_test_bg_listener_off(test_env, subtests)