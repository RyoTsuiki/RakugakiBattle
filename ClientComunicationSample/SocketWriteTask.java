import java.io.DataOutputStream;
import javafx.concurrent.Task;

public class SocketWriteTask extends Task<Void> {	// callメソッドの戻り値をVoid型になるように宣言
	//送信するメッセージ
	private String my_message 	= null;
	private DataOutputStream dos 	= null;

	public SocketWriteTask(DataOutputStream dos) {	//コンストラクタで値を初期化
		this.dos = dos;
	}

	@Override
	protected Void call() throws Exception{
		while(true){
			//メッセージがあれば
			if (my_message != null && !my_message.equals(null)){
				//読み込んだメッセージをサーバーに送信
				this.dos.write(my_message.getBytes());
				this.dos.flush();
				this.my_message = null;
			}
			if(isCancelled()) break;
		}
		return null;
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