module main;

import std.stdio;
import std.algorithm;
import std.array;
import std.datetime;
import std.file;
import tkd.tkdapplication;


class Application : TkdApplication
{

	/**
	 * Initialise the user interface.
	 */
	override protected void initInterface()
	{
		this.mainWindow.setTitle("Tkd Showcase");
		this.mainWindow.setMinSize(550, 560);
		//this.mainWindow.setDefaultIcon([new EmbeddedPng!("tkicon.png")]);
		
		
		
		
		auto exitButton = new Button("Exit")
			.setCommand(&this.exitApplication)
			.pack(5);
	}

	/**
	 * Exit the application.
	 *
	 * Params:
	 *     args = The command arguments.
	 */
	private void exitApplication(CommandArgs args)
	{
		this.exit();
	}
}


void main(string[] args)
{
	auto app = new Application();
	app.run();
	// writeln("Edit source/app.d to start your project.");
}
