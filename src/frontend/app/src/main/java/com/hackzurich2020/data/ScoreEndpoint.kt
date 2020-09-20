package com.hackzurich2020.data

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST


interface ScoreEndpoint {

    @POST("score")
    fun getAllScores(@Body body: List<String>): Call<ScoresResponse>
}