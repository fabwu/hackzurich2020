package com.hackzurich2020

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.recyclerview.widget.LinearLayoutManager
import com.hackzurich2020.data.Query
import com.hackzurich2020.data.ScoreEndpoint
import com.hackzurich2020.data.ScoresResponse
import com.hackzurich2020.data.ServiceBuilder
import kotlinx.android.synthetic.main.activity_dishes_scores.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class DishesScoresActivity : AppCompatActivity(), OnScoreItemClickListener {
    override fun onItemClick(query: Query) {
        val bottomSheet = ScoreDetailsBottomSheetDialog()
        val bundle = Bundle()
        bundle.putString("water", query.indicators.environment.water_footprint_rating)
        bundle.putString("animal", query.indicators.environment.animal_treatment_rating)
        bundle.putString("forest", query.indicators.environment.rainforest_rating)
        bundle.putString("ecosystem", query.indicators.environment.season_rating)
        bottomSheet.arguments = bundle
        bottomSheet.show(supportFragmentManager, "bottomSheet")
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_dishes_scores)
        getAllScores()
    }


    private fun getAllScores() {
        val body = listOf(
            "Red-Thai-Curry",
            "Spaghetti-carbonara",
            "Caesar-Salad",
            "Wiener-Schnitzel"
        )
        val request = ServiceBuilder.buildService(ScoreEndpoint::class.java)
        val call = request.getAllScores(body)
        Log.i("ScoresActivity", "start")

        call.enqueue(object : Callback<ScoresResponse> {
            override fun onResponse(
                call: Call<ScoresResponse>,
                response: Response<ScoresResponse>
            ) {
                if (response.isSuccessful) {
                    animationView.visibility=View.GONE
                    recyclerView.apply {
                        setHasFixedSize(true)
                        layoutManager = LinearLayoutManager(this@DishesScoresActivity)
                        adapter = ScoreAdapter(response.body()!!.queries, this@DishesScoresActivity)
                    }
                }
            }

            override fun onFailure(call: Call<ScoresResponse>, t: Throwable) {
                animationView.visibility=View.GONE

                Toast.makeText(this@DishesScoresActivity, "${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }
}
