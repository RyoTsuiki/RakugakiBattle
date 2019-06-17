import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;
import android.os.AsyncTask;


public class SocketTask extends AsyncTask<String , String, String> {	// callメソッドの戻り値をVoid型になるように宣言

	/**ストリーム*/
	private DataInputStream 		dis = null;
	private DataOutputStream 		dos = null;
	private Boolean 			finish	= false;

	/**送信用タスク、呼び出し元*/
	public SocketWriteTask 		writer;
	private MainActivity  			root;

	//コンストラクタで値を初期化
	public SocketTask(MainActivity root) {
		this.root 	= root;
	}

	protected void interpretation_message(String message){
		String[] messages = message.split(",");
		switch (messages[0]) {
			case Protocol.GAMEDATA:
				// 式の値と値Aが一致したときの処理
				String odai	= messages[1];
				String id	= messages[2];
				break;
			case Protocol.RESULT:
				// 式の値と値Bが一致したときの処理
				int 	score 	= Integer.parseInt(messages[1]);
				String 	rank 	= messages[2];
				break;
			default:
				// 式の値がどのcaseの値とも一致しなかったときの処理

		}
	}

	@Override
	protected String doInBackground(String[] param)  {
		// 引数から接続先サーバのホスト名またはIPアドレスを取得
		String serverIp = param[0];
		// 引数からポート番号を取得
		int portNumb = Integer.parseInt(param[1]);

		// 指定されたホスト名（IPアドレス）とポート番号でサーバに接続する
		Socket socket = null;
		try {
			socket = new Socket();
			socket.connect(new InetSocketAddress(serverIp, portNumb));

			// 接続されたソケットの入力ストリームを取得し，データ入力ストリームを連結
			dis = new DataInputStream(socket.getInputStream());
			dos = new DataOutputStream(socket.getOutputStream());

			//送信用スレッド作成、実行
			writer = new SocketWriteTask(dos);
			Thread thread = new Thread(writer);
			thread.start();
			System.out.println("connected" + " " + serverIp);
			//受信するデータを格納する配列
			byte[] bytesMessage = new byte[4098];

			// データを受信してメッセージを解釈する関数に与える
			while((dis.read(bytesMessage, 0, 4098)) != -1){
				String message = new String(bytesMessage, "UTF-8");
				//受け取ったメッセージをデバッグメッセージとして標準出力に
				System.out.println(message);
				interpretation_message(message);

				//メッセージ初期化
				bytesMessage = new byte[4098];
				//キャンセルされたら終了
				if(finish) 		break;
				if(isCancelled()) 	break;
			}
			//ソケット関連のエラーを想定
		} catch (Exception e) {
			//エラーの表示
			System.out.println(String.valueOf(e));
		} finally {
			if (socket != null) {
				try {
					//送信スレッドの終了
					writer.finish();
					//ソケットを閉じる
					socket.close();
				} catch (IOException e) {
					System.out.println(String.valueOf(e));
				}
			}
		}
		return null;
	}
	@Override
	protected  void onPreExecute(){}
	@Override
	protected void onProgressUpdate(String... values) {}

	@Override
	protected void onPostExecute(String result) {}

	//スレッドを終わる
	public void finish(){
		this.finish = true;
	}
}
