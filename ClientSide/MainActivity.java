package c.example.sample;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    Button resetButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //リセットボタンで画面をリセットさせる
        resetButton = (Button) findViewById(R.id.resetButton);
        resetButton.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.resetButton:
                PaintView paintView = (PaintView) findViewById(R.id.view);
                paintView.clear(); //画面をクリアに
                break;
        }
    }
}