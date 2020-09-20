package com.hackzurich2020.data

import com.google.gson.annotations.SerializedName


data class ScoresResponse(
    val queries: List<Query>
)

data class Query(
    val indicators: Indicators,
    @SerializedName("matched-ingredients")
    val matched_ingredients: List<MatchedIngredient>,
    @SerializedName("matched-recipe")
    val matched_recipe: String,
    val query: String
)

data class Indicators(
    @SerializedName("co2-eq-in-g")
    val co2_eq_in_g: Int,
    @SerializedName("environment")
    val environment: Environment,
    val rating: String
)

data class MatchedIngredient(
    val amount: Double,
    val lang: String,
    val name: String,
    val unit: String
)

data class Environment(
    @SerializedName("animal-treatment-label")
    val animal_treatment_label: Boolean,
    @SerializedName("animal-treatment-rating")
    val animal_treatment_rating: String,
    @SerializedName("local-label")
    val local_label: Boolean,
    @SerializedName("local-rating")
    val local_rating: String,
    @SerializedName("rainforest-label")
    val rainforest_label: Boolean,
    @SerializedName("rainforest-rating")
    val rainforest_rating: String,
    @SerializedName("season-label")
    val season_label: Boolean,
    @SerializedName("season-rating")
    val season_rating: String,
    @SerializedName("water-footprint-award")
    val water_footprint_award: Boolean,
    @SerializedName("water-footprint-rating")
    val water_footprint_rating: String
    )