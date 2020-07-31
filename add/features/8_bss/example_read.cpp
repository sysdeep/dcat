// read a file into memory
// gcc main.cpp -o app -lstdc++
#include <iostream>     // std::cout
#include <fstream>      // std::ifstream
#include <string>

int buffToInteger(char * buffer, int offset=0)
{
    //int a = static_cast<int>(static_cast<unsigned char>(buffer[0]) << 24 |
    //    static_cast<unsigned char>(buffer[1]) << 16 |
    //    static_cast<unsigned char>(buffer[2]) << 8 |
    //    static_cast<unsigned char>(buffer[3]));

    //int a = int((unsigned char)(buffer[0]) << 24 |
    //        (unsigned char)(buffer[1]) << 16 |
    //        (unsigned char)(buffer[2]) << 8 |
    //        (unsigned char)(buffer[3]));

    int a = int((unsigned char)(buffer[0+offset])  |
            (unsigned char)(buffer[1+offset]) << 8 |
            (unsigned char)(buffer[2+offset]) << 16 |
            (unsigned char)(buffer[3+offset]) << 24);

    return a;
}

std::string buffToStr(char * buffer, int offset, int len){

	char * tmp = new char [len];
	int tmp_i = 0;
	for(int i=offset; i<offset+len; i++){
		tmp[tmp_i] = buffer[i];
		tmp_i++;
	}

	std::string s( reinterpret_cast< char const* >(tmp) ) ;

	delete[] tmp;

	return s;
}

void unpackHeader(char * buffer){
	int version = buffToInteger(buffer);
	std::cout << "Header version: " << version << std::endl;

	int created = buffToInteger(buffer, 4);
	std::cout << "Header created: " << created << std::endl;

	int icon = buffToInteger(buffer, 4 + 4);
	std::cout << "Header icon: " << icon << std::endl;

	int name_len = buffToInteger(buffer, 4 + 4 + 4);
	//std::cout << "Header name_len: " << name_len << std::endl;

	std::string name = buffToStr(buffer, 4 + 4 + 4 + 4, name_len);
	std::cout << "Header name: " << name << std::endl;

	int description_len = buffToInteger(buffer, 4 + 4 + 4 + 4 + name_len);
	//std::cout << "Header description_len: " << description_len << std::endl;

	std::string description = buffToStr(buffer, 4 + 4 + 4 + 4 + name_len + 4, description_len);
	std::cout << "Header description: " << description << std::endl;
}


int main () {

  std::ifstream is ("Video.bss", std::ifstream::binary);
  if (is) {
    // get length of file:
    is.seekg (0, is.end);
    int length = is.tellg();
    is.seekg (0, is.beg);

	std::cout << "Reading " << 4 << " characters... " << std::endl;
	char * header_len_buffer = new char [4];
	is.read(header_len_buffer, 4);

	// int header_len = (int)header_len_buffer;
	int header_len = buffToInteger(header_len_buffer);
	std::cout << "Header len: " << header_len << std::endl;
	delete[] header_len_buffer;


	char * header_buffer = new char [header_len];
	is.read(header_buffer, header_len);

	unpackHeader(header_buffer);


	delete[] header_buffer;

//    char * buffer = new char [length];

//    std::cout << "Reading " << length << " characters... ";
//    // read data as a block:
//    is.read (buffer,length);

//    if (is)
//      std::cout << "all characters read successfully.";
//    else
//      std::cout << "error: only " << is.gcount() << " could be read";
    is.close();

    // ...buffer contains the entire file...

//    delete[] buffer;

  }
  return 0;
}
