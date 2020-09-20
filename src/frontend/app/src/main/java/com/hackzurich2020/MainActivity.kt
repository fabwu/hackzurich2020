package com.hackzurich2020

import android.app.Activity
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Rect
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.provider.MediaStore
import android.util.Log
import android.view.View
import android.widget.Toast
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.content_main.*

class MainActivity : AppCompatActivity(), MainPresenter.View {

    private lateinit var mainPresenter: MainPresenter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        mainPresenter = MainPresenter(this)
        dispatchTakePictureIntent()
    }

    private fun dispatchTakePictureIntent() {
        val intent = Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
        startActivityForResult(intent, 1)
//        Intent(MediaStore.ACTION_IMAGE_CAPTURE).also { takePictureIntent ->
//            takePictureIntent.resolveActivity(packageManager)?.also {
//                startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE)
//            }
//        }
    }


    override fun onActivityResult(requestCode: Int, resultCode: Int, imageReturnedIntent: Intent?) {
        super.onActivityResult(requestCode, resultCode, imageReturnedIntent)
        when (requestCode) {
            1 -> if (resultCode == Activity.RESULT_OK) {
                Log.i("ImageScanner", (imageReturnedIntent?.data != null).toString())
                imageReturnedIntent?.data?.let {
                    val selectedImageBitmap = resizeImage(it)
                    imageView.setImageBitmap(selectedImageBitmap)
                    overlay.clear()
                    mainPresenter.runTextRecognition(selectedImageBitmap!!)
                }
            }
        }
    }

    private fun resizeImage(selectedImage: Uri): Bitmap? {
        return getBitmapFromUri(selectedImage)?.let {
            val scaleFactor = Math.max(
                it.width.toFloat() / imageView.width.toFloat(),
                it.height.toFloat() / imageView.height.toFloat()
            )

            Bitmap.createScaledBitmap(
                it,
                (it.width / scaleFactor).toInt(),
                (it.height / scaleFactor).toInt(),
                true
            )
        }
    }

    private fun getBitmapFromUri(filePath: Uri): Bitmap? {
        return MediaStore.Images.Media.getBitmap(this.contentResolver, filePath)
    }

    override fun showHandle(text: String, boundingBox: Rect?) {
        overlay.addText(text, boundingBox)
    }

    override fun showBox(boundingBox: Rect?) {
        overlay.addBox(boundingBox)
    }


    override fun showNoTextMessage() {
        Toast.makeText(this, "No text detected", Toast.LENGTH_LONG).show()
    }

    override fun showProgress() {
        progressBar.visibility = View.VISIBLE
    }

    override fun hideProgress() {
        progressBar.visibility = View.GONE
        startActivity(Intent(this, DishesScoresActivity::class.java))
    }
}
