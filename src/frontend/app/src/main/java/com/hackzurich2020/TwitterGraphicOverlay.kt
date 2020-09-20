/*
 *
 * Copyright (c) 2018 Razeware LLC
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * Notwithstanding the foregoing, you may not use, copy, modify, merge, publish,
 * distribute, sublicense, create a derivative work, and/or sell copies of the
 * Software in any work that is designed, intended, or marketed for pedagogical or
 * instructional purposes related to programming, coding, application development,
 * or information technology.  Permission for such use, copying, modification,
 * merger, publication, distribution, sublicensing, creation of derivative works,
 * or sale is expressly withheld.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

package com.hackzurich2020

import android.content.Context
import android.content.Intent
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Rect
import android.net.Uri
import android.util.AttributeSet
import android.view.View
import com.hackzurich2020.TextGraphic
import java.util.*

/**
 * Adapted from the ML Kit Google code lab
 * https://codelabs.developers.google.com/codelabs/mlkit-android/#0
 */

class TwitterGraphicOverlay(context: Context, attrs: AttributeSet) : View(context, attrs) {

  private val lock = Any()
  private val graphics = HashSet<Graphic>()
  private val handles = mutableListOf<TwitterGraphicOverlay.Handle>()

  init {
    setOnTouchListener { _, event ->
      openTwitterIfProfileClicked(event.x, event.y)
    }
  }

  private fun openTwitterIfProfileClicked(x: Float, y: Float): Boolean {
    return handles.find { it.boundingBox?.contains(x.toInt(), y.toInt()) ?: false }?.let {
      openTwitterProfile(it.text)
      true
    } ?: run {
      false
    }
  }

  private fun openTwitterProfile(handle: String) {
    val url = "https://twitter.com/" + handle.trim().removePrefix("@")
    val browserIntent = Intent(Intent.ACTION_VIEW,
        Uri.parse(url))
    context.startActivity(browserIntent)
  }

  /**
   * Base class for a custom graphics object to be rendered within the graphic overlay. Subclass
   * this and implement the [Graphic.draw] method to define the graphics element. Add
   * instances to the overlay using [TwitterGraphicOverlay.add].
   */
  abstract class Graphic(private val overlay: TwitterGraphicOverlay) {

    /**
     * Draw the graphic on the supplied canvas. Drawing should use the following methods to convert
     * to view coordinates for the graphics that are drawn:
     *
     *
     *
     *
     * @param canvas drawing canvas
     */
    abstract fun draw(canvas: Canvas)

    fun postInvalidate() {
      overlay.postInvalidate()
    }
  }

  /**
   * Removes all graphics from the overlay.
   */
  fun clear() {
    synchronized(lock) {
      graphics.clear()
    }
    postInvalidate()
  }

  /**
   * Adds a graphic to the overlay.
   */
  private fun add(graphic: Graphic) {
    synchronized(lock) {
      graphics.add(graphic)
    }
    postInvalidate()
  }

  class Handle(val text: String, val boundingBox: Rect?)

  fun addText(text: String, boundingBox: Rect?) {
    add(TextGraphic(this, boundingBox))
    handles.add(Handle(text, boundingBox))
  }

  fun addBox(boundingBox: Rect?) {
    add(TextGraphic(this, boundingBox, Color.RED))
  }

  /**
   * Draws the overlay with its associated graphic objects.
   */
  override fun onDraw(canvas: Canvas) {
    super.onDraw(canvas)

    synchronized(lock) {
      for (graphic in graphics) {
        graphic.draw(canvas)
      }
    }
  }
}