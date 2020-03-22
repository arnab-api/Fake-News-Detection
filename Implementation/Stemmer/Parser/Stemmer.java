package Parser;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;

public class Stemmer {

	public static void main(String[] args) {

		String ruleFilePath = "C:/Users/User/Dropbox/0Thesis Combined/Stemmer/common.rules";

		File InFolder = new File("./Inputs");
		File[] InFiles = InFolder.listFiles();

		for (int i = 0; i < InFiles.length; i++) {
			if (InFiles[i].isFile()) {
			
				String inputFilePath = InFiles[i].getAbsolutePath();

				String outputFilePath = "./Outputs/"+InFiles[i].getName();

				RuleFileParser parser = new RuleFileParser(ruleFilePath);

				File inFile = new File(inputFilePath);
				File outFile = new File(outputFilePath);

				try (BufferedReader inputFileReader = new BufferedReader(new FileReader(inFile))) {
					String line;
					BufferedWriter outputFileWriter = new BufferedWriter(new FileWriter(outFile));
					while ((line = inputFileReader.readLine()) != null) {
						for (String word : line.split("[\\s।%,ঃ]+")) {
							outputFileWriter.write(parser.stemOfWord(word) + " ");
						}
						outputFileWriter.write("\n");
					}
					outputFileWriter.close();
				} catch (IOException exception) {
					exception.printStackTrace();
				}

			}
		}
	}
}