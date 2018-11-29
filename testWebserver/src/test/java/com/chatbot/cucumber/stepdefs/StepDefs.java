package com.chatbot.cucumber.stepdefs;

import com.chatbot.TestWebserverApp;

import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.test.web.servlet.ResultActions;

import org.springframework.boot.test.context.SpringBootTest;

@WebAppConfiguration
@SpringBootTest
@ContextConfiguration(classes = TestWebserverApp.class)
public abstract class StepDefs {

    protected ResultActions actions;

}
