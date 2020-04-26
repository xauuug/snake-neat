<h1 align="center">Snake-NEAT</h1><br>
<p align="center">
  <img alt="Snake-NEAT" title="Snake-NEAT" src="https://i.imgur.com/BDdGfBC.gif" width="450"><br>
</p>

<h4 align="center">A self-learning snake game implemented using NEAT algorithm</h4>

## About

Project developed at the college as a final work for the artificial intelligence subject

> Original code developed between May 15, 2018 - Jun 29, 2018

## How to run

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python game.py
```

## Dependencies

* **[Pygame](https://github.com/pygame/)**: Used in game development and user interaction
* **[neat-python](https://github.com/CodeReclaimers/neat-python)**: Python implementation of the NEAT neuroevolution algorithm

## Controls

* **F1**: Takes control of the game, making it possible to control the snake's movements with the keyboard arrows
* **F2**: Sets a high frame rate (fast) until the snake dies
* **F3**: Sets a low frame rate (slow) until the snake dies
* **F4**: Enable the debug draw, drawing input indicators

## Fitness function

```python
SnakeLength - TurnedQuantity * 0.01
```

* **SnakeLength**: Snake length defined by how many apples it ate

* **TurnedQuantity**: How many times did the snake change direction, either left or right

## Inputs

1. **cd_left**: Collision-free units at left
2. **cd_top**: Collision-free units at top
3. **cd_right**: Collision-free units at right
4. **cd_bottom**: Collision-free units at bottom
5. **cd_top_left**: Collision-free units at top left
6. **cd_top_right**: Collision-free units at top right
7. **cd_bottom_left**: Collision-free units at bottom left
8. **cd_bottom_right**: Collision-free units at bottom right
9. **apple_x_distance**: If there is an apple on the right or left, this variable contains the distance in units to the apple
10. **apple_y_distance**: If there is an apple on the top or bottom, this variable contains the distance in units to the apple

> You can "see" these inputs in debug mode

<p align="center">
  <img alt="Debug Mode" title="Debug Mode" src="https://i.imgur.com/m60tMox.gif" width="450"><br>
</p>

## Outputs

* **0**: Don't change direction
* **1**: Turn right
* **2**: Turn left
