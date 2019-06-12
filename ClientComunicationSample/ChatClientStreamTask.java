/*
 * 学籍番号：150441087
 * 氏名　　：對木　良
 * クラス　：B
 */
package jp.ac.meijo_u.id150441087.chat;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;

import javafx.concurrent.Task;

public class ChatClientStreamTask extends Task<Void> {	// callメソッドの戻り値をVoid型になるように宣言
	/** ipアドレス、ポート*/
	private String 				ip;
	private String 				port;

	/**ストリーム*/
	private DataInputStream 		dis = null;
	private DataOutputStream 		dos = null;

	/**送信用タスク、呼び出し元*/
	private ChatClientWriteTask 	writeTask;
	private ChatClientController 	root;

	//コンストラクタで値を初期化
	public ChatClientStreamTask(String ip, String port, ChatClientController root) {
		this.ip 	= ip;
		this.port 	= port;
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
			int score 	= Integer.parseInt(messages[1]);
			int rank 	= Integer.parseInt(messages[2]);
		    break;
		default:
		    // 式の値がどのcaseの値とも一致しなかったときの処理

		}
	}

	@Override
	protected Void call()  {
		// 変数からIPアドレス、ポートを取得
		String serverIp = ip;
		int portNumb = Integer.parseInt(port);

		// 指定されたホスト名（IPアドレス）とポート番号でサーバに接続する
		Socket socket = null;
		try {
			socket = new Socket();
			socket.connect(new InetSocketAddress(serverIp, portNumb));

			// 接続されたソケットの入力ストリームを取得し，データ入力ストリームを連結
			dis = new DataInputStream(socket.getInputStream());
			dos = new DataOutputStream(socket.getOutputStream());

			//送信用スレッド作成、実行
			writeTask = new ChatClientWriteTask(dos);
			Thread thread = new Thread(writeTask);
			thread.setDaemon(true);
			thread.start();

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
				if(isCancelled()) break;
			}
		//ソケット関連のエラーを想定
		} catch (Exception e) {
			//エラーの表示
			updateMessage(String.valueOf(e));
		} finally {
			if (socket != null) {
				try {
					//送信スレッドの終了
					writeTask.cancel();
					//ソケットを閉じる
					socket.close();
				} catch (IOException e) {
					updateMessage(String.valueOf(e));
				}
			}
		}
		return null;
	}
}