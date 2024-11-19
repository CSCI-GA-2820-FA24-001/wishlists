# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa

"""
Web Steps

Steps file for web interactions with Selenium

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constants for element ID prefixes
WISHLIST_PREFIX = "wishlist_"
ITEM_PREFIX = "item_"

######################################################################
# Navigation and Verification Steps
######################################################################


@when('I visit the "Home Page"')
def step_impl(context):
    """Make a call to the base URL"""
    context.driver.get(context.base_url)
    # Uncomment next line to take a screenshot of the web page
    # context.driver.save_screenshot('home_page.png')


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """Check the document title for a message"""
    assert message in context.driver.title


@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    element = context.driver.find_element(By.TAG_NAME, "body")
    assert text_string not in element.text


######################################################################
# Input Steps
######################################################################


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Set an input field with appropriate prefix"""
    # Determine if this is a wishlist or item field
    if "Item" in element_name:
        element_id = ITEM_PREFIX + element_name.lower().replace("item ", "").replace(
            " ", "_"
        )
    else:
        element_id = WISHLIST_PREFIX + element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)


@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Select from a dropdown with appropriate prefix"""
    if "Item" in element_name:
        element_id = ITEM_PREFIX + element_name.lower().replace("item ", "").replace(
            " ", "_"
        )
    else:
        element_id = WISHLIST_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(context.driver.find_element(By.ID, element_id))
    element.select_by_visible_text(text)


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    if "Item" in element_name:
        element_id = ITEM_PREFIX + element_name.lower().replace("item ", "").replace(
            " ", "_"
        )
    else:
        element_id = WISHLIST_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(context.driver.find_element(By.ID, element_id))
    assert element.first_selected_option.text == text


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    if "Item" in element_name:
        element_id = ITEM_PREFIX + element_name.lower().replace("item ", "").replace(
            " ", "_"
        )
    else:
        element_id = WISHLIST_PREFIX + element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute("value") == ""


##################################################################
# Copy/Paste Steps
##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    if "Item" in element_name:
        element_id = ITEM_PREFIX + element_name.lower().replace("item ", "").replace(
            " ", "_"
        )
    else:
        element_id = WISHLIST_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute("value")
    logging.info("Clipboard contains: %s", context.clipboard)


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    if "Item" in element_name:
        element_id = ITEM_PREFIX + element_name.lower().replace("item ", "").replace(
            " ", "_"
        )
    else:
        element_id = WISHLIST_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)


##################################################################
# This code works because of the following naming convention:
# The buttons have an id in the html hat is the button text
# in lowercase followed by '-btn' so the Clear button has an id of
# id='clear-btn'. That allows us to lowercase the name and add '-btn'
# to get the element id of any button
##################################################################


@when('I press the "{button}" button')
def step_impl(context, button):
    """Click a button using its text"""
    button_id = button.lower().replace(" ", "-") + "-btn"
    context.driver.find_element(By.ID, button_id).click()


@then('I should see "{text}" in the wishlist results')
def step_impl(context, text):
    """Verify text in search results"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "search_results"), text)
    )
    assert found


@then('I should see "{text}" in the item results')
def step_impl(context, text):
    """Verify text in item results"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "items_list"), text)
    )
    assert found


@then('I should not see "{text}" in the wishlist results')
def step_impl(context, text):
    element = context.driver.find_element(By.ID, "search_results")
    assert text not in element.text


@then('I should not see "{text}" in the item results')
def step_impl(context, text):
    element = context.driver.find_element(By.ID, "items_list")
    assert text not in element.text


@then('I should see the message "{message}"')
def step_impl(context, message):
    """Verify flash message"""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), message)
    )
    assert found


##################################################################
# Field Content Steps
# This code works because of the following naming convention:
# The id field for text input in the html is the element name
# prefixed by ID_PREFIX so the Name field has an id='item_name'
# We can then lowercase the name and prefix with item_ to get the id
##################################################################


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    """Verify a field is empty"""
    if "Item" in element_name:
        element_id = ITEM_PREFIX + element_name.lower().replace("item ", "").replace(
            " ", "_"
        )
    else:
        element_id = WISHLIST_PREFIX + element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute("value") == ""


@then('I should see "{text}" in the "{element_name}" field')
def step_impl(context, text, element_name):
    """Verify text in a field"""
    if "Item" in element_name:
        element_id = ITEM_PREFIX + element_name.lower().replace("item ", "").replace(
            " ", "_"
        )
    else:
        element_id = WISHLIST_PREFIX + element_name.lower().replace(" ", "_")
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element_value((By.ID, element_id), text)
    )
    assert found


@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    if "Item" in element_name:
        element_id = ITEM_PREFIX + element_name.lower().replace("item ", "").replace(
            " ", "_"
        )
    else:
        element_id = WISHLIST_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)


######################################################################
# Custom Steps for Items
######################################################################


@when('I retrieve the "{wishlist_name}" wishlist')
def step_impl(context, wishlist_name):
    """Retrieve a specific wishlist"""
    context.execute_steps(
        f"""
        When I set the "Name" to "{wishlist_name}"
        And I press the "Search" button
        And I press the "Retrieve" button
    """
    )


@when('I select item "{item_name}" in the results')
def step_impl(context, item_name):
    """Select an item from the results list"""
    # Wait for the item to be present in the list
    WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.CLASS_NAME, "edit-item"))
    )
    # Find and click the edit button for the specific item
    items = context.driver.find_elements(
        By.XPATH, f"//td[contains(text(), '{item_name}')]"
    )
    if items:
        edit_button = items[0].find_element(
            By.XPATH, "..//button[contains(@class, 'edit-item')]"
        )
        edit_button.click()
