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
import field.Field;
import field.ShapeType;

/**
 * Shape class
 * 
 * Represents the shapes that appear in the field.
 * Some basic methods have already been implemented, but
 * actual move actions, etc. should still be created.
 * 
 * @author Jim van Eeden <jim@riddles.io>
 */

public class Shape {

	private ShapeType type;
	private Cell[][] shape; // 2-dimensional bounding box: a matrix that contains the block-cells of the shape
	private Cell[] blocks; // array that contains only the block-cells of the shape
	private int size;
	private Point location;
	private Field field;
	private int uniqueRot;
	
	public Shape(ShapeType type, Field field, Point location) {
		this.type = type;
		this.field = field;
		this.blocks = new Cell[4];
		this.location = location;
		
		setShape();
		setBlockLocations();
	}
	
	// ACTIONS (no checks for errors are performed in the actions!)
	
	/**
	 * Rotates the shape counter-clockwise
	 */
	public void turnLeft() {
		Cell[][] temp = this.transposeShape();

		for (int y = 0; y < this.size; y++) {
			for (int x = 0; x < this.size; x++) {
				this.shape[x][y] = temp[x][this.size - y - 1];
			}
		}
		
		this.setBlockLocations();
	}
	
	/**
	 * Rotates the shape clockwise
	 */
	public void turnRight() {
		Cell[][] temp = this.transposeShape();

		for (int x = 0; x < this.size; x++) {
			this.shape[x] = temp[this.size - x - 1];
		}
		
		this.setBlockLocations();
	}
	
	public void oneDown() {
		this.location.y++;
		this.setBlockLocations();
	}

	public void oneUp(){
		this.location.y--;
		this.setBlockLocations();
	}
	
	public void oneRight() {
		this.location.x++;
		this.setBlockLocations();
	}
	
	public void oneLeft() {
		this.location.x--;
		this.setBlockLocations();
	}
	
	/**
	 * Used for rotations
	 * @return transposed matrix of current shape box
	 */
	private Cell[][] transposeShape() {
		Cell[][] temp = new Cell[this.size][this.size];

		for (int y = 0; y < this.size; y++) {
			for( int x = 0; x < this.size; x++) {
				temp[y][x] = this.shape[x][y];
			}
		}

		return temp;
	}
	
	/**
	 * Uses the shape's current orientation and position to
	 * set the actual location of the block-type cells on the field
	 */
	private void setBlockLocations() {
		for (int y = 0; y < this.size; y++) {
			for (int x = 0; x < this.size; x++) {
				if (this.shape[x][y].isShape()) {
                    this.shape[x][y].setLocation(this.location.x + x, this.location.y + y);
				}
			}
		}
	}
	
	/** 
	 * Set shape in square box.
	 * Creates new Cells that can be checked against the actual
     * playing field.
     * */
	private void setShape() {
		switch (this.type) {
			case I:
				this.size = 4;
				this.uniqueRot = 2;
				this.shape = initializeShape();
				this.blocks[0] = this.shape[0][1];
				this.blocks[1] = this.shape[1][1];
				this.blocks[2] = this.shape[2][1];
				this.blocks[3] = this.shape[3][1];
				break;
			case J:
				this.size = 3;
				this.uniqueRot = 4;
				this.shape = initializeShape();
				this.blocks[0] = this.shape[0][0];
				this.blocks[1] = this.shape[0][1];
				this.blocks[2] = this.shape[1][1];
				this.blocks[3] = this.shape[2][1];
				break;
			case L:
				this.size = 3;
				this.uniqueRot = 4;
				this.shape = initializeShape();
				this.blocks[0] = this.shape[2][0];
				this.blocks[1] = this.shape[0][1];
				this.blocks[2] = this.shape[1][1];
				this.blocks[3] = this.shape[2][1];
				break;
			case O:
				this.size = 2;
				this.uniqueRot = 1;
				this.shape = initializeShape();
				this.blocks[0] = this.shape[0][0];
				this.blocks[1] = this.shape[1][0];
				this.blocks[2] = this.shape[0][1];
				this.blocks[3] = this.shape[1][1];
				break;
			case S:
				this.size = 3;
				this.uniqueRot = 2;
				this.shape = initializeShape();
				this.blocks[0] = this.shape[1][0];
				this.blocks[1] = this.shape[2][0];
				this.blocks[2] = this.shape[0][1];
				this.blocks[3] = this.shape[1][1];
				break;
			case T:
				this.size = 3;
				this.uniqueRot = 4;
				this.shape = initializeShape();
				this.blocks[0] = this.shape[1][0];
				this.blocks[1] = this.shape[0][1];
				this.blocks[2] = this.shape[1][1];
				this.blocks[3] = this.shape[2][1];
				break;
			case Z:
				this.size = 3;
				this.uniqueRot = 2;
				this.shape = initializeShape();
				this.blocks[0] = this.shape[0][0];
				this.blocks[1] = this.shape[1][0];
				this.blocks[2] = this.shape[1][1];
				this.blocks[3] = this.shape[2][1];
				break;
		}
		
		// set type to SHAPE
        for (Cell block : this.blocks) {
            block.setShape();
        }
	}
	
	/**
	 * Creates the matrix for the shape
	 */
	private Cell[][] initializeShape() {
		Cell[][] newShape = new Cell[this.size][this.size];

		for (int y = 0; y < this.size; y++) {
			for (int x = 0; x < this.size; x++) {
				newShape[x][y] = new Cell();
			}
		}

		return newShape;
	}
	
	
	public void setLocation(int x, int y) {
		this.location = new Point(x, y);
		this.setBlockLocations();
	}
	
	public Cell[] getBlocks() {
		return this.blocks;
	}
	
	public Point getLocation() {
		return this.location;
	}
	
	public ShapeType getType() {
		return this.type;
	}

	public int getStartColumn() {
		int minX = 11;
		for (int i = 0; i<blocks.length; i++){
			if (blocks[i].getLocation().x<minX){
				minX=blocks[i].getLocation().x;
			}
		}
		return minX-this.getLocation().x;
	}

	public int getUniqueRot() {
		return uniqueRot;
	}
}
