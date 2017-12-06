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

package field;

import java.awt.Point;

import field.Cell;
import field.Shape;

/**
 * Field class
 * 
 * Represents the playing field for one player.
 * Has some basic methods already implemented.
 * 
 * @author Jim van Eeden <jim@riddles.io>
 */

public class Field {
	
	private int width;
	private int height;
	private Cell grid[][];

	public Field(int width, int height, String input) {
	    this.width = width;
	    this.height = height;

	    parseFromString(input);
    }
	
	/**
	 * Parses the input string to get a grid with Cell objects
	 * @param input input string
	 */
	private void parseFromString(String input) {
		this.grid = new Cell[this.width][this.height];
		int x = 0;
		int y = 0;

		for (String cellString : input.split(",|;")) {
		    int cellCode = Integer.parseInt(cellString.trim());
		    this.grid[x][y] = new Cell(x, y, CellType.values()[cellCode]);

		    if (++x == this.width) {
		        x = 0;
		        y++;
            }
        }
	}
	
	public Cell getCell(int x, int y) {
		if (x < 0 || x >= this.width || y < 0 || y >= this.height) {
			return null;
		}

		return this.grid[x][y];
	}
	
	public int getHeight() {
		return this.height;
	}
	
	public int getWidth() {
		return this.width;
	}

	public boolean canPlaceShape(Shape shape){
		Cell[] blocks = shape.getBlocks();
		for (int i = 0; i<blocks.length; i++){
			if (blocks[i].isOutOfBoundaries(this) || blocks[i].hasCollision(this)){
				return false;
			}
		}
		return true;
	}

	public boolean addShape(Shape shape){
		if (!this.canPlaceShape(shape)){
			return false;
		}
		Cell[] blocks = shape.getBlocks();
		for (int i = 0; i<blocks.length; i++){
			this.grid[blocks[i].getLocation().x][blocks[i].getLocation().y].setShape();
		}
		return true;
	}

	public boolean removeShape(Shape shape){
		Cell[] blocks = shape.getBlocks();
		for (int i = 0; i<blocks.length; i++){
			this.grid[blocks[i].getLocation().x][blocks[i].getLocation().y].setEmpty();
		}
		return true;
	}

	public float calculateHeuristicWithShape(Shape shape){
		if (!addShape(shape)){
			return 999999999;
		}
		float hVal = calculateHeuristic();
		removeShape(shape);
		return hVal;
	}

	public float calculateHeuristic(){
		int aggregateHeight = 0;
		int numHoles = 0;
		int lineClears = 0;
		for (int x = 0; x < width; x++){
			boolean foundBlock = false;
			for (int y = 0; y<height; y++){
				if (!foundBlock && !grid[x][y].isEmpty()){
					foundBlock=true;
					aggregateHeight+=height-1-y;
				} else if (foundBlock && grid[x][y].isEmpty()){
					numHoles++;
				}
			}
		}
		for (int y = 0; y<height; y++){
			boolean clear = true;
			for (int x=0; x<width; x++){
				if (!(this.grid[x][y].isBlock() || this.grid[x][y].isShape())){
					clear=false;
				}
			}
			if (clear){
				lineClears++;
			}
		}
		return (aggregateHeight+numHoles*4)/(lineClears+1);
	}


	public void clearTop(){
		for (int x = 0; x<width; x++){
			if (this.grid[x][0].isShape()){
				this.grid[x][0].setEmpty();
			}
		}
	}
}
