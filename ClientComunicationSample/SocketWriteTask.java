import java.io.*;

public class SocketWriteTask implements Runnable {	// callメソッドの戻り値をVoid型になるように宣言
	//送信するメッセージ
	private String my_message 	= null;
	private DataOutputStream dos 	= null;
	private Boolean finish 		= false;
	public SocketWriteTask(DataOutputStream dos) {	//コンストラクタで値を初期化
		this.dos = dos;
	}

	@Override
	public void run() {
		while (true) {
			if (my_message != null && !my_message.equals(null)) {
				try {
					//読み込んだメッセージをサーバーに送信
					this.dos.write(my_message.getBytes());
					this.dos.flush();
					this.my_message = null;
				} catch (Exception e) {
					System.out.println(e);
					break;
				}
				if(finish) break;
			}
		}
	}
	//スレッドを終わる
	public void finish(){
		this.finish = true;
	}
	//開始メッセージを送る
	public void send_start_game(String name){
		String message = Protocol.STARTGAME + "," + name;
		this.my_message = message;
	}

	//終了メッセージを送る
	public void send_end_game(){
		String message = Protocol.ENDGAME;
		this.my_message = message;
	}

	//オリジナルのメッセージを送る
	public void send_original_message(String message){
		this.my_message = message;
	}

}
