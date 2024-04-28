import java.io.*;
import java.net.*;
import java.util.Scanner;
import java.util.NoSuchElementException;

public class TCPClient {

    private static final int MAX_LINE = 256;
    private String host;
    private int serverPort;
    private Socket socket;
    private PrintWriter out;
    private Scanner userInput;

    public TCPClient(String host, int serverPort) {
        this.host = host;
        this.serverPort = serverPort;
    }

    public void connect() throws IOException {
        socket = new Socket(host, serverPort);
        out = new PrintWriter(socket.getOutputStream(), true);
        userInput = new Scanner(System.in);
    }

    public void sendMessage(String message) throws IOException {
        if (message != null && !message.isEmpty()) {
            if (message.length() > MAX_LINE - 2) {
                message = message.substring(0, MAX_LINE - 2);
            }
            message += "\n\0";
            out.print(message);
            out.flush();
        }
    }

    public String receiveMessage() throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        String response = in.readLine();
        return response;
    }

    public void processMessages() throws IOException {
        String line;
        while (true) {
            line = userInput.nextLine();
            if (line.equals("\u0004")) {
                this.closeConnection();
                break;
            }
            sendMessage(line);

            String response = receiveMessage();
            if (response != null) {
                System.out.println("Server says: " + response);
            }
        }
    }

    public void closeConnection() throws IOException {
        out.close();
        userInput.close();
        socket.close();
    }

    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Usage: java TCPClient <server_host> <server_port>");
            System.exit(1);
        }

        String host = args[0];
        int serverPort = Integer.parseInt(args[1]);

        try {
            TCPClient client = new TCPClient(host, serverPort);
            client.connect();
            System.out.println(
                    "Connected to the server. Type messages, press enter to send, 'ctrl+d' or 'ctrl+c' to quit.");
            client.processMessages();
        } catch (UnknownHostException e) {
            System.err.println("tcp_client: Don't know about host " + host);
            System.exit(1);
        } catch (IOException e) {
            System.err.println("tcp_client: Couldn't get I/O for the connection to " + host);
            System.exit(1);
        } catch (NoSuchElementException e) {
            System.err.println("tcp_client: Connection closed by client.");
            System.exit(1);
        }
    }
}