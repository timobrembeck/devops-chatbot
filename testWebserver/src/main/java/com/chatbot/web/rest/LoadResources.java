package com.chatbot.web.rest;

import com.codahale.metrics.annotation.Timed;
import com.google.gson.Gson;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.resource.HttpResource;

@RestController
@RequestMapping("/api/load")
public class LoadResources {

    @Autowired
    private static final Gson gson = new Gson();

    @GetMapping("/medium")
    @Timed
    public ResponseEntity<String> mediumLoad() {

        double sum=0;

        for(double i=0; i<300000000L; i++)
        {
            if(i%2 == 0) // if the remainder of `i/2` is 0
                sum += -1 / ( 2 * i - 1);
            else
                sum += 1 / (2 * i - 1);
        }

        return ResponseEntity.ok(gson.toJson(Double.toString(sum)));
    }

    @GetMapping("/full")
    @Timed
    public ResponseEntity<String> fullLoad() {


        double sum=0;

        for(int j=0; j<=10; j++) {

            for (double i = 0; i < 1000000000L; i++) {
                if (i % 2 == 0) // if the remainder of `i/2` is 0
                    sum += -1 / (2 * i - 1);
                else
                    sum += 1 / (2 * i - 1);
            }

        }

        return ResponseEntity.ok(gson.toJson(Double.toString(sum)));

    }
}
