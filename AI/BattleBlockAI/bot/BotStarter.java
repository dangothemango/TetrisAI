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

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

import moves.Move;
import moves.MoveType;
import field.Shape;
import field.Field;
/**
 * BotStarter class
 * 
 * This class is where the main logic should be. Implement getMove() to
 * return something better than random moves.
 * 
 * @author Jim van Eeden <jim@riddles.io>
 */

public class BotStarter {

	private Random random;

	public BotStarter() {
		this.random = new Random();
	}
	
	/**
	 * Returns a random amount of random moves
	 * @param state current state of the bot
	 * @return a list of moves to execute
	 */
	public Move getMove(BotState state) {
		List<MoveType> allMoves = Collections.unmodifiableList(Arrays.asList(MoveType.values()));
		MoveType move = null;

        ArrayList<MoveType> moves = getPathToBestMove(state);
		
		return new Move(moves);
	}
	
	public static void main(String[] args) {
		BotParser parser = new BotParser(new BotStarter());
		parser.run();
	}

	private ArrayList<MoveType> getPathToBestMove(BotState state){
		Field field = state.getPlayers().get(state.getMyName()).getField();
		field.clearTop();
		Shape shape = new Shape(state.getCurrentShape(),field,state.getShapeLocation());
		int startPosition = shape.getLocation().x;

		//TODO: enable rotations
		float maxH = 9999999;
		int maxLoc = -1;
		int maxRot = -1;
		for (int rot =0; rot<shape.getUniqueRot(); rot++){
			for (int i = 0-shape.getStartColumn(); i<field.getWidth(); i++){
				shape.setLocation(i,-1);
				while (field.canPlaceShape(shape)){
					shape.oneDown();
				}
				shape.oneUp();
				if (!field.canPlaceShape(shape)) continue;
				float t = field.calculateHeuristicWithShape(shape);
				if ( t < maxH ){
					maxH = t;
					maxLoc = i;
					maxRot = rot;
				}
			}
			shape.turnRight();
		}

		ArrayList<MoveType> moves = new ArrayList<MoveType>();
		if (maxRot==3){
			moves.add(MoveType.TURNLEFT);
		} else {
			for (int i = 0; i < maxRot; i++){
				moves.add(MoveType.TURNRIGHT);
			}
		}
		while (startPosition != maxLoc){
			if (startPosition<maxLoc){
				moves.add(MoveType.RIGHT);
				startPosition++;
			} else {
				moves.add(MoveType.LEFT);
				startPosition--;
			 }
		}
		moves.add(MoveType.DROP);
		return moves;
	}
}
