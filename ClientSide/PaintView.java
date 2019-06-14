package c.example.sample;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Path;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;

import java.util.ArrayList;

public class PaintView extends View {

    private Paint paint;
    private Path path;

    public PaintView(Context context) {
        super(context);
    }

    public PaintView(Context context, AttributeSet attrs) { //AttributeSetでAttributeにsetできるようにする
        super(context, attrs);

        //画面に線を書くためのPaintとPathを用意する
        paint = new Paint();
        path = new Path();

        //線の色や開始終了の形を決める
        paint.setColor(0xFF000000); //線の色を黒に
        paint.setStyle(Paint.Style.STROKE);
        paint.setStrokeJoin(Paint.Join.ROUND); //線のつなぎ目を丸く
        paint.setStrokeCap(Paint.Cap.ROUND); //線の端面を丸く
        paint.setStrokeWidth(10);
    }

    //線描画メソッド
    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        //画面を描画するときに用意したpathとpaintを使用するようにする
        canvas.drawPath(path, paint);
    }

    //画面をTouchしたら描くようにする
    @Override
    public boolean onTouchEvent(MotionEvent event) {

        //Touchしたx座標とy座標を取得
        float x = event.getX();
        float y = event.getY();

        //各Touchイベントの種類ごとに動きを決める
        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN: //Touchしたとき
                path.moveTo(x, y);
                invalidate(); //OnDrawメソッドを呼び出している。OnDrawメソッドを呼び出すのはなぜかinvalidate()
                break;
            case MotionEvent.ACTION_MOVE: //Touchしたまま動かしたとき
            case MotionEvent.ACTION_UP: //Touchを離したとき
                path.lineTo(x, y);
                invalidate();
                break;
        }

        return true;

    }

    //描いた絵を削除するメソッド。resetButtonクリック時に呼ばれる
    public void clear() {
        path.reset();
        invalidate();
    }
}
