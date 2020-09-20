package com.hackzurich2020

import android.graphics.Bitmap
import android.graphics.Rect
import com.google.firebase.ml.vision.FirebaseVision
import com.google.firebase.ml.vision.cloud.FirebaseVisionCloudDetectorOptions
import com.google.firebase.ml.vision.cloud.text.FirebaseVisionCloudText
import com.google.firebase.ml.vision.common.FirebaseVisionImage
import com.google.firebase.ml.vision.text.FirebaseVisionText

/**
 * Created by Amr on 9/19/2020.
 */
class MainPresenter(val view: View) {
    private val dishes = mutableListOf<String>()

    fun runTextRecognition(selectedImage: Bitmap) {
        view.showProgress()
        val image = FirebaseVisionImage.fromBitmap(selectedImage)
        val detector = FirebaseVision.getInstance().visionTextDetector
        detector.detectInImage(image)
            .addOnSuccessListener { texts ->
                processTextRecognitionResult(texts)
            }
            .addOnFailureListener { e ->
                // Task failed with an exception
                e.printStackTrace()
            }
    }

    private fun processTextRecognitionResult(texts: FirebaseVisionText) {
        view.hideProgress()
        val blocks = texts.blocks
        if (blocks.size == 0) {
            view.showNoTextMessage()
            return
        }
        blocks.forEach { block ->
            block.lines.forEach { line ->
                line.elements.forEach { element ->
                    if (looksLikeHandle(element.text)) {
                        dishes.add(element.text)
                        view.showHandle(element.text, element.boundingBox)
                    }
                }
            }
        }
    }


    fun getScannedDishes() = dishes
    // this for cloud features
    fun runCloudTextRecognition(selectedImage: Bitmap) {
        view.showProgress()
        val options = FirebaseVisionCloudDetectorOptions.Builder()
            .setModelType(FirebaseVisionCloudDetectorOptions.LATEST_MODEL)
            .setMaxResults(15)
            .build()
        val image = FirebaseVisionImage.fromBitmap(selectedImage)
        val detector = FirebaseVision.getInstance()
            .getVisionCloudDocumentTextDetector(options)
        detector.detectInImage(image)
            .addOnSuccessListener { texts ->
                processCloudTextRecognitionResult(texts)
            }
            .addOnFailureListener { e ->
                e.printStackTrace()
            }
    }

    class WordPair(val word: String, val handle: FirebaseVisionCloudText.Word)

    private fun processCloudTextRecognitionResult(text: FirebaseVisionCloudText?) {
        view.hideProgress()
        if (text == null) {
            view.showNoTextMessage()
            return
        }
        text.pages.forEach { page ->
            page.blocks.forEach { block ->
                block.paragraphs.forEach { paragraph ->
                    paragraph.words
                        .zipWithNext { a, b ->
                            val word = wordToString(a) + wordToString(b)
                            WordPair(word, b)
                        }
                        .filter {
                            looksLikeHandle(it.word)
                        }
                        .forEach {
                            view.showHandle(it.word, it.handle.boundingBox)
                        }
                }
            }
        }
    }

    private fun wordToString(
        word: FirebaseVisionCloudText.Word
    ): String =
        word.symbols.joinToString("") { it.text }

    private fun looksLikeHandle(text: String) = true
    //text.matches(Regex("#(\\w+)"))


    interface View {
        fun showNoTextMessage()
        fun showHandle(text: String, boundingBox: Rect?)
        fun showBox(boundingBox: Rect?)
        fun showProgress()
        fun hideProgress()
    }
}