package com.rctf.hellodalvik;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {
    private String[] angry = new String[]{"6F50D5057EFB2B9411C1B237E7D8588D", "98DD67FE3789D499AB3AF3CD1055EB76", "10556D767F835C91A9B2BBCF98DDE4FE", "72AD4A98C3603EE1865407ACFA25C210"};
    private String code = "a#s224kfuSaom=D469asSkOdhmP34!@-";
    private int G;
    private int B;
    private int C;
    private int D;
    private String hexChars = "0123456789ABCDEF";
    private int F;
    private int E;
    private char[] code_chars;
    private int bytemask = 255;
    private int A;

    public native int stringFromJNI();

    public MainActivity() {
        System.loadLibrary("native-lib");
        Log.d("Have Fine! ", stringFromJNI() + "");
    }

    protected void onCreate(Bundle savedInstanceState) {
        final String[] kk = new String[1];
        super.onCreate(savedInstanceState);
        setContentView((int) R.layout.activity_main);
        init_code_chars();
        final TextView tv = (TextView) findViewById(R.id.sample_text);
        final EditText editText = (EditText) findViewById(R.id.editText);
        ((Button) findViewById(R.id.button)).setOnClickListener(new OnClickListener() {
            public void onClick(View v) {
                String flag = "";
                int check = 0;
                char[] here = String.valueOf(editText.getText()).toCharArray();
                for (int k = 0; k < here.length; k++) {
                    if (k % 3 == 0) {
                        String s = "";
                        for (int ff = 0; ff < 3; ff++) {
                            s = s + here[(k + ff) % here.length];
                        }
                        kk[0] = MainActivity.this.merge(MainActivity.this.box1to1(s), s);
                        if (kk[0].equals(MainActivity.this.angry[(k / 3) % 4])) {
                            flag = flag + s;
                        } else {
                            tv.setText("Too Young!!");
                            check = 1;
                        }
                    }
                }
                if (check == 0) {
                    tv.setText("RCTF{" + flag + "}");
                }
            }
        });
    }

    private char[] box1to1(String a) {
        char[] result = new char[32];
        char[] aa = a.toCharArray();
        for (int k = 0; k < aa.length; k++) {
            aa[k] = (char) (aa[k] % 10);
        }
        for (int i = 0; i < 32; i++) {
            this.A = new MathMethod().MathMethod_3(i, aa.length);
            this.B = new MathMethod().MathMethod_3(i, this.code_chars.length);
            this.C = new MathMethod().MathMethod_4(this.B, aa[this.A]);
            this.D = new MathMethod().MathMethod_1(this.C, this.code_chars[this.B]);
            this.E = new MathMethod().MathMethod_2(this.C, this.D);
            this.F = new MathMethod().MathMethod_5(this.D, this.code_chars[this.A]);
            this.G = new MathMethod().MathMethod_4(this.E, this.F);
            result[i] = (char) (this.G & this.bytemask);
        }
        return result;
    }

    private String merge(char[] a, String b) {
        String result = "";
        if (a.length != 32) {
            return null;
        }
        char[] ss = b.toCharArray();
        char[] gg = this.hexChars.toCharArray();
        for (int k = 0; k < ss.length; k++) {
            ss[k] = (char) ((ss[k] / 10) % 10);
        }
        for (int i = 0; i < 32; i++) {
            result = result + gg[(ss[i % ss.length] + a[i]) % 16];
        }
        return result;
    }

    private void init_code_chars() {
        this.code_chars = this.code.toCharArray();
    }
}