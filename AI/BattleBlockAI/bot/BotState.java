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

import java.awt.Point;
import java.util.HashMap;
import java.util.Map;

import player.Player;

import field.Field;
import field.ShapeType;

/**
 * BotState class
 * 
 * In this class all the information about the game is stored.
 * 
 * @author Jim van Eeden <jim@riddles.io>
 */

public class BotState {

	private int roundNumber;
	private int timebank;
	private HashMap<String, Player> players;
	private String myName;
	private ShapeType currentShape;
	private ShapeType nextShape;
	private Point shapeLocation;

	private int MAX_TIMEBANK;
	private int TIME_PER_MOVE;
	private int FIELD_WIDTH;
	private int FIELD_HEIGHT;

	public BotState() {
		this.roundNumber = 0;
		this.players = new HashMap<>();
	}

	public void setTimebank(int value) {
		this.timebank = value;
	}

	public int getTimebank() {
		return this.timebank;
	}

	public int getMaxTimebank() {
		return MAX_TIMEBANK;
	}

	public void setMaxTimebank(int maxTimebank) {
		MAX_TIMEBANK = maxTimebank;
	}

	public int getTimePerMove() {
		return TIME_PER_MOVE;
	}

	public void setTimePerMove(int TimePerMove) {
		TIME_PER_MOVE = TimePerMove;
	}

    public void setFieldWidth(int width) {
        FIELD_WIDTH = width;
    }

    public void setFieldHeight(int height) {
        FIELD_HEIGHT = height;
    }

    public int getFieldHeight() {
        return FIELD_HEIGHT;
    }

    public int getFieldWidth() {
        return FIELD_WIDTH;
    }

	public int getRoundNumber() {
		return this.roundNumber;
	}

	public void setRoundNumber(int roundNumber) {
		this.roundNumber = roundNumber;
	}

	public String getMyName() {
		return this.myName;
	}

	public void setMyName(String myName) {
		this.myName = myName;
	}

	public HashMap<String, Player> getPlayers() {
		return this.players;
	}

	public void setPlayers(HashMap<String, Player> players) {
		this.players = players;
	}

    public ShapeType getCurrentShape() {
        return this.currentShape;
    }

    public void setCurrentShape(ShapeType currentShape) {
        this.currentShape = currentShape;
    }

    public ShapeType getNextShape() {
        return this.nextShape;
    }

    public void setNextShape(ShapeType nextShape) {
        this.nextShape = nextShape;
    }

    public Point getShapeLocation() {
        return this.shapeLocation;
    }

    public void setShapeLocation(Point shapeLocation) {
        this.shapeLocation = shapeLocation;
    }
}