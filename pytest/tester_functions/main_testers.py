from tester_functions.bg_listener_testers import helper_test_bg_listener_on, helper_test_bg_listener_off
from tester_functions.overlay_view_testers import helper_test_overlay_breakout_key_on, helper_test_overlay_breakout_key_off
from tester_functions.cp_view_testers import helper_test_control_panel_key, helper_test_close_control_panel
from tester_functions.latex_window_testers import helper_test_latex_output_enter
from tester_functions.navbar_component_testers import helper_test_navbar
from tester_functions.unicode_window_testers import helper_test_unicode_search_menu, helper_test_unicode_search_function,helper_test_unicode_copy_paste, helper_test_unicode_copy_via_overlay

def bg_listener_tester(test_env, subtests):
    
    helper_test_bg_listener_on(test_env, subtests)
    
    helper_test_bg_listener_off(test_env, subtests)

def overlay_tester(test_env, subtests):

    # Turn on the overlay
    helper_test_bg_listener_on(test_env, subtests)

    helper_test_overlay_breakout_key_on(test_env, subtests)

    helper_test_overlay_breakout_key_off(test_env, subtests)

#     helper_test_overlay_init(test_env, subtests)

#     helper_test_overlay_key(test_env, subtests)

#     # This will be run right after test_overlay_key()
#     # Thus, Ctrl + D has already been pressed and overlay is on
#     helper_test_exit_key(test_env, subtests)

#     helper_test_wrong_key(test_env, subtests)
    
#     helper_test_control_panel_key(test_env, subtests)

#     helper_test_close_control_panel(test_env)

#     # Redo all of the overlay tests
#     helper_test_overlay_init(test_env, subtests)

#     helper_test_overlay_key(test_env, subtests)

#     # This will be run right after test_overlay_key()
#     # Thus, Ctrl + D has already been pressed and overlay is on
#     helper_test_exit_key(test_env, subtests)

#     helper_test_wrong_key(test_env, subtests)

# def latex_tester(test_env, subtests):
    
#     helper_test_overlay_init(test_env, subtests)

#     helper_test_control_panel_key(test_env, subtests)

#     helper_test_latex_output_enter(test_env, subtests)

# def navbar_tester(test_env, subtests):
    
#     helper_test_overlay_init(test_env, subtests)

#     helper_test_control_panel_key(test_env, subtests)

#     helper_test_navbar(test_env, subtests)

# def unicode_tester(test_env, subtests):

#     helper_test_unicode_search_menu(test_env, subtests)

#     helper_test_unicode_search_function(subtests)

#     helper_test_unicode_copy_paste(subtests)

#     helper_test_unicode_copy_via_overlay(test_env, subtests)