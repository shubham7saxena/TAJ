/*
C socket server example
*/
#include <stdio.h>
#include <string.h> //strlen
#include <sys/socket.h>
#include <arpa/inet.h> //inet_addr
#include <unistd.h> //write
#include <bits/stdc++.h>
#include "dist/json/json.h"
#include "dist/jsoncpp.cpp"
#include <sys/time.h>
#include <iostream>
#include <string>
#include <sstream>
#include <iostream>
#include <fstream>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <signal.h>
#include <sys/resource.h> 
#include <sys/wait.h>
#include <curl/curl.h>
#include <fstream>
#include <sys/mman.h>

#define MAX 1000

using namespace std;

int compare_files();

static int *glob_var;


void sig_handler(int signo)
{
 	// if (signo == SIGINT )
	 //    cout << "Received Signal\n";

  	if (signo == SIGXCPU)
  		cout << "Recieved Time Limit Exceed\n";

  	else cout << "In Function exiting\n";

	close(1);
	close(0);
	close(2);
	exit(55);
}

int getrlimit(int resource, struct rlimit *rlim); 
int setrlimit(int resource, const struct rlimit *rlim);


int main(int argc , char *argv[])
{


	glob_var = (int *) mmap(NULL, sizeof *glob_var, PROT_READ | PROT_WRITE, 
	                    MAP_SHARED | MAP_ANONYMOUS, -1, 0);
	*glob_var = 1;

	pid_t pid = fork();

	if(pid == 0){


			// Signal Handlers

			if (signal(SIGXCPU , sig_handler) == SIG_ERR)
		        printf("\ncan't catch SIGINT\n");

		    if (signal(SIGXFSZ , sig_handler) == SIG_ERR)
		        printf("\ncan't catch SIGINT\n");
		    // if (signal(SIGKILL , sig_handler) == SIG_ERR)
		    //     printf("\ncan't catch SIGINT\n");
		    if (signal(SIGINT , sig_handler) == SIG_ERR)
		        printf("\ncan't catch SIGINT\n");

		    if (signal(SIGSEGV , sig_handler) == SIG_ERR)
		        printf("\ncan't catch SIGINT\n");

			int socket_desc , client_sock , c , read_size;
			struct sockaddr_in server , client;
			char client_message[20000];

			// Create socket
			socket_desc = socket(AF_INET , SOCK_STREAM , 0);
			if (socket_desc == -1)
			{
				printf("Could not create socket");
			}
			puts("Socket created");

			//Prepare the sockaddr_in structure
			server.sin_family = AF_INET;
			server.sin_addr.s_addr = INADDR_ANY;

			// Put here the port number.

			server.sin_port = htons( 6029 );

			//Bind
			if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0)
			{
			//print the error message
				perror("bind failed. Error");
				return 1;
			}
			puts("bind done");

			//Listen
			listen(socket_desc , 3);

			//Accept and incoming connection
			puts("Waiting for incoming connections...");
			c = sizeof(struct sockaddr_in);

			//accept connection from an incoming client
			client_sock = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c);
			if (client_sock < 0)
			{
				perror("accept failed");
				return 1;
			}
			puts("Connection accepted");

			Json::Value root;   
			Json::Reader reader;

			//Receive a message from client
			while( (read_size = recv(client_sock , client_message , 20000 , 0)) > 0 )
			{
			//Send the message back to client
				// std:: cout << " Strlen : " << strlen(client_message) << std::endl;


				bool parsingSuccessful = reader.parse( client_message, root );     //parse process
				    if ( !parsingSuccessful )
				    {
				        std::cout  << "Failed to parse"
				               << reader.getFormattedErrorMessages();
				        return 0;
				    }
				    // std::cout << root.get("hello", "A Default Value if not exists" ).asString() << std::endl;
				    // cout << client_message << endl;

				   	//Parsing of the function json received:
				   	// 	 temp = simplejson.dumps({
					   	//   'id': sol.id, 
			      		//	'path' : str(os.getcwd()),
			      		//	'filename': str(name[:-4]),
			      		//	'input': input,
			      		//	'output': output,
			      		//  'time': p.timeLimit})
			}	

			if(read_size == 0)
			{
				puts("Client disconnected");
				fflush(stdout);
			}
			else if(read_size == -1)
			{
				perror("recv failed");
			}

			int time_limit = root.get("time", "5").asInt();
			string filename = root.get("filename", "error").asString();
			string input = root.get("input", "").asString();
			string output = root.get("output", "5").asString();
			string path = root.get("filepath", "5").asString();
			int sol_id = root.get("sol_id", "2").asInt();
			*glob_var = sol_id; 

			// cout << "Path : " << path <<endl;

			std::ofstream file("input.txt");
			file << input;
			file.close();


			// Clearing the data from 
			std::ofstream ofs;
			ofs.open("output.txt", std::ofstream::out | std::ofstream::trunc);
			ofs.close();

			ofs.open("out.txt", std::ofstream::out | std::ofstream::trunc);
			ofs.close();

			std::ofstream file_o("output.txt");
			file_o << endl << endl;
			file_o << output;
			file_o.close();

		// Child Process
		int file_read = open("input.txt", O_RDWR | O_CREAT, S_IRUSR | S_IWUSR);
		int file_write = open("out.txt", O_RDWR | O_CREAT, S_IRUSR | S_IWUSR);

		dup2(file_read, 0);
		dup2(file_write, 1);   // make stdout go to file
		dup2(file_write, 2);   // make stderr go to file - you may choose to not do this
		               // or perhaps send stderr to another file

		close(file_write);     // file_write no longer needed - the dup'ed handles are sufficient
		close(file_read); 

		// Setting Up Resource Limit.

		struct rlimit rl; 
		// time_limit = 1;
		// First get the time limit on CPU 
		getrlimit (RLIMIT_CPU, &rl); 
		
		// printf("\n Default value is : %lld\n", (long long int)rl.rlim_cur); 
		
		// Change the time limit 
		rl.rlim_cur = time_limit + 1; 
		rl.rlim_max = time_limit + 1; 
		// Now call setrlimit() to set the  
		// changed value. 

		setrlimit (RLIMIT_CPU, &rl); 
		
		// Again get the limit and check 
		getrlimit (RLIMIT_CPU, &rl); 
		
		// printf("\n Default value now is : %lld %lld\n", (long long int)rl.rlim_cur, (long long int)rl.rlim_max); 
		
		// char ww*	 = path.c_str();
		// char * args[] = {(char *)path.c_str() , NULL};
		// char *const args[] = {argv[1] , NULL};
	    // char * envs[] = {"LD_PRELOAD=./EasySandbox.so", NULL};


	    char *const args[] = {(char *)path.c_str(), NULL};
	    // char *const args[] = {"./trial", NULL};
	    char * envs[] = {"LD_PRELOAD=./EasySandbox.so", NULL};
	    // execve("./trial",args,envs);



	    // cout << "Path : " << path << endl;
	    // sleep(1);
	    execve( (char *) path.c_str(), args, envs);
	    // execve( "./trial", args, envs);

	    perror("execve");
	    exit(5);
	}

	else{

	

		/////////////////////////////////////////////////////////////////////////////////
		//////////////////////////////////////////////////////////////////

		int status = 5;
		if ( waitpid(pid, &status, 0) == -1 ) {
		    perror("waitpid failed");
		    return EXIT_FAILURE;
		}

		if ( WIFEXITED(status) ) {
		    const int es = WEXITSTATUS(status);
		    printf("exit status was %d\n", es);
		}

		cout << "Stats : " << status << endl;


		/////////////////////////////////////////////////////////////////////////////////
		//////////////////////////////////////////////////////////////////

		// Compare output Files.....

		int result = compare_files();

		cout << "Results : " << result << endl;

		string result_str;
		// files not matching
		if(!result) result_str = "5";
		else result_str = "4";
		/////////////////////////////////////////////////////////////////////////////////
		//////////////////////////////////////////////////////////////////


		/////////////////////////////////////////////////////////////////////////////////
		////////////////////// CURL REQUEST /////////////////////////////////////////////

		CURL *curl;
		CURLcode res;

		string url = "http://127.0.0.1:8000/judge/trail/";

		int xx = *glob_var;
		string sol_id_string = to_string(xx);
		// cout << sol_id_string << "*" << endl;
		url += "?sol_id=";
		url += sol_id_string;

		url += "&result=";
		url += result_str;

		// cout << url;
		curl = curl_easy_init();
		if(curl) {
		  curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
		  /* example.com is redirected, so we tell libcurl to follow redirection */ 
		  // curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
		
		  /* Perform the request, res will get the return code */ 
		  res = curl_easy_perform(curl);
		  /* Check for errors */ 
		  if(res != CURLE_OK)
		    fprintf(stderr, "curl_easy_perform() failed: %s\n",
		            curl_easy_strerror(res));
		
		  /* always cleanup */ 
		  curl_easy_cleanup(curl);
		}

		munmap(glob_var, sizeof *glob_var);



	return 0;

	}
	return 0;
}


int compare_files(){
  ifstream infile, sourcefile;
	char c,s;
	bool flag_s = false, flag_i = false;
	
	sourcefile.open("out.txt");
	infile.open("output.txt");
	// Check open file error !
	if(sourcefile.fail()) {
		cout << "Error opending source file !";
		return 0;
	}
	if(infile.fail()) {
		cout << "Error opending compare file !";
		return 0;
	}
	while(1){
		sourcefile >> s;
		infile >> c;
		if(sourcefile.eof()) flag_s = true;
		if(infile.eof()) flag_i = true;
		
		if((flag_s != flag_i)||(s!=c)){

			cout << "Not Match !" << s << " " << c;
			break;
		}else if(flag_s||flag_i) {
			cout << "Match !";
			sourcefile.close();
			infile.close();
			return 1;
			break;
		}	
	}
	sourcefile.close();
	infile.close();
	return 0;
}
