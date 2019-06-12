import java.io.DataOutputStream;
import javafx.concurrent.Task;

public class ChatClientWriteTask extends Task<Void> {	// callメソッドの戻り値をVoid型になるように宣言
	//送信するメッセージ
	private static String my_message 	= null;
	private static DataOutputStream dos 	= null;

	public ChatClientWriteTask(DataOutputStream dos) {	//コンストラクタで値を初期化
		ChatClientWriteTask.dos = dos;
	}

	@Override
	protected Void call() throws Exception{
		while(true){
			//メッセージがあれば
			if (my_message != null && !my_message.equals(null)){
				//読み込んだメッセージをサーバーに送信
				dos.write(my_message.getBytes());
				dos.flush();
				my_message = null;
			}
			if(isCancelled()) break;
		}
		return null;
	}

	//開始メッセージを送る
	public static void send_start_game(String name){
		String message = Protocol.STARTGAME + "," + name;
		my_message = message;
	}

	//終了メッセージを送る
	public static void send_end_game(){
		String message = Protocol.ENDGAME;
		my_message = message;
	}

	//オリジナルのメッセージを送る
	public static void send_original_message(String message){
		my_message = message;
	}

}
