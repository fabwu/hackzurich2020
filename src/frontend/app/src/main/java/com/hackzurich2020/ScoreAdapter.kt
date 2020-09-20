package com.hackzurich2020

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.hackzurich2020.data.Query


class ScoreAdapter(val results: List<Query>,val listener: OnScoreItemClickListener) :
    RecyclerView.Adapter<ScoreAdapter.ScoreViewHolder>() {


    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ScoreViewHolder {
        val view =
            LayoutInflater.from(parent.context).inflate(R.layout.item_dish_score, parent, false)
        return ScoreViewHolder(view)
    }

    override fun getItemCount(): Int {
        return results.size
    }

    override fun onBindViewHolder(holder: ScoreViewHolder, position: Int) {
        return holder.bind(results[position])
    }

    inner class ScoreViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView)  {


        private val dishName: TextView = itemView.findViewById(R.id.dish_name)
        private val dishCo2: TextView = itemView.findViewById(R.id.dish_co2)
        private val rating: TextView = itemView.findViewById(R.id.rating)


        fun bind(query: Query) {
            dishName.text = query.query
            dishCo2.text = query.indicators.co2_eq_in_g.toString() + " g"
            rating.text = query.indicators.rating
            itemView.setOnClickListener{
                listener.onItemClick(query = query)
            }
        }


    }
}