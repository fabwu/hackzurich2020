package com.hackzurich2020

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.google.android.material.bottomsheet.BottomSheetDialogFragment
import kotlinx.android.synthetic.main.bottom_sheet_persistent.*


class ScoreDetailsBottomSheetDialog : BottomSheetDialogFragment() {

    fun newInstanse(): ScoreDetailsBottomSheetDialog {
        return ScoreDetailsBottomSheetDialog()
    }


    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        val view = inflater.inflate(R.layout.bottom_sheet_persistent, container, false)

        return view
    }

    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)
        val water: String? = arguments?.getString("water")
        val animal = arguments?.getString("animal")
        val forest = arguments?.getString("forest")
        val ecosystem = arguments?.getString("ecosystem")
        waterBar.progress = caculateRating(water ?: "A")
        animalBar.progress = caculateRating(animal ?: "A")
        forestBar.progress = caculateRating(forest ?: "A")
        ecosystemBar.progress = caculateRating(ecosystem ?: "A")
    }

    private fun caculateRating(rating: String): Int {
        return when (rating) {
            "A" -> 20
            "B" -> 40
            "C" -> 60
            "D" -> 80
            else -> 100

        }
    }

}