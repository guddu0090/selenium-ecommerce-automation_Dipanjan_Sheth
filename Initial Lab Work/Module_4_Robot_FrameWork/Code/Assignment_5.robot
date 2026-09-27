*** Settings ***
Library     SeleniumLibrary

*** Variables ***
${URL}        https://rahulshettyacademy.com/AutomationPractice/
${BROWSER}    Edge

*** Test Cases ***
Handle Alert And Take Screenshot
    Open Browser                 ${URL}                       ${BROWSER}
    Maximize Browser Window

    Input Text                   id=name                      angshul

    Click Element                id=alertbtn
    Handle Alert                 accept

    Capture Page Screenshot      selenium-screenshot-1.png

    Close Browser
