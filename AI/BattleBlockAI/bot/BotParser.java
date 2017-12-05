/*
 *  Copyright 2016 riddles.io (developers@riddles.io)
 *
 *      Licensed under the Apache License, Version 2.0 (the "License");
 *      you may not use this file except in compliance with the License.
 *      You may obtain a copy of the License at
 *
 *          http://www.apache.org/licenses/LICENSE-2.0
 *
 *      Unless required by applicable law or agreed to in writing, software
 *      distributed under the License is distributed on an "AS IS" BASIS,
 *      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *      See the License for the specific language governing permissions and
 *      limitations under the License.
 *
 *      For the full copyright and license information, please view the LICENSE
 *      file that was distributed with this source code.
 */

package bot;

import java.awt.*;
import java.util.Arrays;
import java.util.Scanner;

import field.Field;
import field.ShapeType;
import moves.Move;
import moves.MoveType;
import player.Player;

/**
 * BotParser class
 * 
 * Main class that will keep reading output from the engine.
 * Will either update the bot state or get actions.
 * 
 * @author Jim van Eeden <jim@riddles.io>
 */

public class BotParser {
	
	private final Scanner scan;
	private final BotStarter bot;
	private BotState currentState;
	
	public BotParser(BotStarter bot)
	{
		this.scan = new Scanner(System.in);
		this.bot = bot;
		this.currentState = new BotState();
	}
	
	public void run()
	{
		while(scan.hasNextLine())
		{
			String line = scan.nextLine().trim();
			if(line.length() == 0) { continue; }
			String[] parts = line.split(" ");
			switch(parts[0]) {
				case "settings":
					parseSettings(parts[1], parts[2]);
					break;
				case "update":
                    if (parts[1].equals("game")) {
                        parseGameData(parts[2], parts[3]);
                    } else {
                        parsePlayerData(parts[1], parts[2], parts[3]);
                    }
					break;
				case "action":
                    this.currentState.setTimebank(Integer.parseInt(parts[2]));
					Move move = this.bot.getMove(this.currentState);

					if (move != null) {
					    System.out.println(move.toString());
                    } else {
					    System.out.println("pass");
                    }

					break;
				default:
				    System.out.println("unknown command");
                    break;
			}
		}
	}

    /**
     * Parses all the game settings given by the engine
     * @param key type of data given
     * @param value value
     */
	private void parseSettings(String key, String value) {
	    try {
            switch (key) {
                case "timebank":
                    int time = Integer.parseInt(value);
                    this.currentState.setMaxTimebank(time);
                    this.currentState.setTimebank(time);
                    break;
                case "time_per_move":
                    this.currentState.setTimePerMove(Integer.parseInt(value));
                    break;
                case "player_names":
                    Arrays.stream(value.split(",")).
                            forEach(name -> {
                                Player player = new Player(name);
                                this.currentState.getPlayers().put(name, player);
                            });
                    break;
                case "your_bot":
                    this.currentState.setMyName(value);
                    break;
                case "field_width":
                    this.currentState.setFieldWidth(Integer.parseInt(value));
                    break;
                case "field_height":
                    this.currentState.setFieldHeight(Integer.parseInt(value));
                    break;
                default:
                    System.err.println(String.format(
                            "Cannot parse settings input with key '%s'", key));
            }
        } catch (Exception e) {
            System.err.println(String.format(
                    "Cannot parse settings value '%s' for key '%s'", value, key));
            e.printStackTrace();
        }
	}

    /**
     * Parse data about the game given by the engine
     * @param key type of data given
     * @param value value
     */
    private void parseGameData(String key, String value) {
        try {
            switch(key) {
                case "round":
                    this.currentState.setRoundNumber(Integer.parseInt(value));
                    break;
                case "this_piece_type":
                    this.currentState.setCurrentShape(ShapeType.valueOf(value));
                    break;
                case "next_piece_type":
                    this.currentState.setNextShape(ShapeType.valueOf(value));
                    break;
                case "this_piece_position":
                    this.currentState.setShapeLocation(parsePoint(value));
                    break;
                default:
                    System.err.println(String.format(
                            "Cannot parse game data input with key '%s'", key));
            }
        } catch (Exception e) {
            System.err.println(String.format(
                    "Cannot parse game data value '%s' for key '%s'", value, key));
            e.printStackTrace();
        }
    }

    /**
     * Parse data about given player that the engine has sent
     * @param playerName player the data is about
     * @param key type of data given
     * @param value value
     */
    private void parsePlayerData(String playerName, String key, String value) {
        Player player = this.currentState.getPlayers().get(playerName);

        if (player == null) {
            System.err.println(String.format("Could not find player with name %s", playerName));
            return;
        }

        try {
            switch (key) {
                case "row_points":
                    player.setPoints(Integer.parseInt(value));
                    break;
                case "combo":
                    player.setCombo(Integer.parseInt(value));
                    break;
                case "skips":
                    player.setSkips(Integer.parseInt(value));
                    break;
                case "field":
                    int fieldWidth = this.currentState.getFieldWidth();
                    int fieldHeight = this.currentState.getFieldHeight();
                    player.setField(new Field(fieldWidth, fieldHeight, value));
                    break;
                default:
                    System.err.println(String.format(
                            "Cannot parse %s data input with key '%s'", playerName, key));
            }
        } catch (Exception e) {
            System.err.println(String.format(
                    "Cannot parse %s data value '%s' for key '%s'", playerName, value, key));
            e.printStackTrace();
        }
    }

    private Point parsePoint(String input) {
        String[] split = input.split(",");
        return new Point(Integer.parseInt(split[0]), Integer.parseInt(split[1]));
    }
}
