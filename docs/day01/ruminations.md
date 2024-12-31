<!-- SPDX-License-Identifier: MIT -->
<!-- Copyright (c) Vojtech Krajnansky -->
# Ruminations: Advent of Code 2015: Day 01
## In Which Santa Learns to Follow Directions
### Part 1
#### 1.1 Thinking About Other Things, Like...
##### 1.1.1 ... Balancing Parentheses and Stacks
This challenge reminds me of the classic problem of **balancing parentheses** - a tale as old as time in computer science<sup>1</sup>, and apparently, as ancient as Santa's milk-and-cookie stash. Often, this problem serves as a nice introdution to **stacks** in CS courses.

Simply put, we want to check whether a sequence of parentheses is balanced, meaning every opening parenthesis has a corresponding closing parenthesis and they are closed in the correct order. 

For example, every `(` must be closed with a corresponding `)`, and every `[` must be closed with a corresponding `]`.

Stacks are an ideal data structure to solve this problem, as they efficiently handle nested structures.

Santa doesn't really care about parentheses balance, but in case you are interested in exploring this a little deeper, here's the pseudocode:

```text
1. Start with an empty stack
2. For each character:
   2.1. If it is an opening char: push onto the stack.
   2.2. If it is a closing char:
      2.2.1. Is stack empty?
         2.2.1.1. We have more closing than opening parentheses - this is unbalanced.
      2.2.2. Otherwise, pop the top stack item, and see if it matches the kind of parenthesis.
3. At the end, do we still have anything left in the stack?
  3.1. If yes, we saw more opening parentheses than closing ones - this is unbalanced.
  3.2. Otherwise, the parentheses are balanced.
```

In the first part of the Day 01 challenge, we are really just concerned with the counts of opening and closing parentheses, which brings us to...

##### 1.1.2 ... Partial Sums and Running Totals
The concept we are dealing with in this problem is much more related to **partial sums** in mathematics. A partial sum is the sum of the first `n` terms of a sequence.

If we have a sequence `[a_1, a_2, ...]`, the partial sum `S_n` is defined as:

`S_n = a_1 + a_2 + ... + a_n`

This is quite useful when working with infinite sequences. The sum of the terms of an infinite sequence is called a **series**. Partial sums allow us to eamine how a series behaves as `n -> inf`. If the sequence of partial sums `[S_n]` approaches some finite limit `S` as `n` approaches infinity, the series converges to `S`. Otherwise, the series diverges.

A practical application<sup>2</sup> is the **running total** (or *cumulative sum*). This is essentially the same as a partial sum, but often in a finite context. It's a note of the total accumulated value as we go through a sequence of numbers. This is exactly what Santa does when he counts the final floor from a sequence of directions.

We use a running total commonly in real-world applications. For example, in finance, a running total may express the cumulative expenses or earnings over time. The balance in your bank account is nothing more but a running total of your personal earnings and expenses. Your bank receives orders, processes them, and keeps a track of the "current state", which is a core component of...

##### 1.1.3 ... Stream Processing
**Stream processing** is a computational paradigm in which we process data in real-time as it is flows in like a *stream*, without needing to store it in a database of some kind. It is useful for handling continuous streams of data from sources like network traffic, logs, or user interactions<sup>3</sup>.

It is usually crucial to maintain a "current state" of some kind, and update it with each incoming piece of data. In the challenge, it is the running sum of the up or down steps. Often, this state takes the form of a running metric, like a cumulative count or a running average.

One typical use case of stream processing is to detect some anomalous state. For example, noticing that a financial transaction is suspicious, or that a warehouse is close to being full as shipments come in quicker than they are sent out.

When reading a sequence of directions, Santa essentially processes the directions as a stream, because not even Santa can keep thousands of instructions in his head at once. It is much easier to simply remember the current sum as a net effect of the individual instructions, which is a good reason to take a slightly more pronounced detour to...

##### 1.1.4 ... Net Effects
The idea of a **net effect** is simple: what's the overall impact when you weigh all the ups and downs<sup>4</sup>. It represents the total, aggregate consequence of actions or decisions. Very useful in decision-making, and an interesting tool for considering ethical implications.

One set of moral beliefs which relies heavily on the concept of net effects is *utilitarianism*, which aims to maximize the overall (or net) happiness of a society. An action is then considered moral if its net effects increase the greatest good for the greatest number.

This sounds great in theory, but there are definitely some other questions to consider. For example, there is the question of individual rights. Sacrificing one person to save a thousand others will have a positive net effect<sup>5</sup>. Buuut, what if you are the one being sacrificed? Doesn't seem so good now, does it?

And of course, not all things in life can be so easily evaluated as contributing positively or negatively to an outcome. And that's why programming is so great - everything is strictly `False` or `True`, a `1`, or a `0`... or is it?

---

<sup>1</sup> In case you didn't know, for computer scientists, time started on *Jan 1st, 1970*.  
<sup>2</sup> Not that partial sums or series are not practical, but they're a lot of... *math*.  
<sup>3</sup> Or a never-ending influx of letters with childrens' wishes, if you're Santa.  
<sup>4</sup> Or `(` and `)`, am I right?  
<sup>5</sup> Oh, trolley problem, my good old friend, you come up in the most unexpected of places.

#### 1.2 Thinking About the Solution
A stream processing approach would be a reasonable solution for this challenge, especially in the input size is expected to be extremely large. Instead of loading the entire file into memory, we could process it incrementally by reading it in chunks (a tumbling window) of characters. This would allow us to maintain a running total, to be returned once we have processed the entire file.

However, for a problem as simple as this, that would definitely count as over-engineering. It is (slightly) easier and (much) more readable to simply read the entire file into memory and analyze its contents in bulk. Modern workstations typically have ample memory to handle files with millions of charactrs - even billions (as long as it's not too many billions).

### Part 2
#### 2.1 Thinking About Other Things, Like...
##### ... Stream Processing - The Sequel
In a real-world scenario where we'd process a stream of instruction data, say, for controlling a drone<sup>6</sup>, we could monitor its current flight level based on how many times it has gone up or down. A flight level of `0` could represent a safety threshold, triggering a reaction like safely landing the drone and turning it off. This works well when the data stream is controlled.

But what if Santa's Directions Officer elf, overcome by a fit of chaotic creativity, starts jotting down random parentheses with reckless abandon? Then, identifying the first moment Santa plunges underground becomes an exercise in calculating...

##### ... First Passage Time
The **first passage time (FPT)** is one of the fundamental concepts in stochastic<sup>7</sup> process analysis. In simple terms, it measures how long a random process takes to reach a specific state.<sup>8</sup> For nerds, here's some math esoterica:

In a stochastic process `{X_t}_t>=0`, the first passage time `T_a` to a target level `a` is defined as:

`T_a = inf{t >= 0: X_t >= a}`, where `X_t` is the state of the process at time `t`.

If `X_t` never reaches `a`, the first passage time is considered infinite.

Why is **FPT** useful? Well, for example, it can help us predict how long it takes stock prices to hit certain levels, describe physical phenomena like diffusion, estimate the time to failure in various systems, and more.

---

<sup>6</sup> Because that's exactly how drones operate, isn't it? Go up `1` step, go down `1` step... No gyroscopic stabilization, no complex algorithms. Nope.
<sup>7</sup> For the longest time, I wondered why math needed 2 different words for *random*, and if people use *stochastic* just to sound smart. Then I found out *stochastic* doesn't actually mean "random". It means "well-described by a random probability distribution". This immediately answered both of my questions: there are two terms because they mean different things; and yes, people most often use *stochastic* to sound smart<sup>9</sup>.  
<sup>8</sup> Mathematicians are invited to take note: This is how real humans speak.
<sup>9</sup> Ironically, they usually don't use it correctly.

#### 2.2 Thinking About the Solution
It is already mentioned in the Solution Design that by validating the directions sequence and computing the required values in a single pass, we could slightly optimize the performance of our program (by about two times the constant factor: `2c`<sup>9</sup>). However, as can be seen in the performance test of `FloorDirectionsAnalysis`, each pass takes less than a second on *my machine*<sup>11</sup> for inputs a thousand times larger than the AoC input, so I prefer not to sacrifice readability and maintainability for any further optimization.

---

<sup>9</sup> This is, in fact, a significant simplification (also known as a "lie") included in the Solution Design for brevity. The actual runtime reduction depends on the probability distribution of the first passage time of the "basement reached" state in Santa's direction following. For instance, if the FPT distribution is uniform, the expected FPT is `0.5c`, resulting in a reduction of `1.5c`<sup>10</sup>.  
<sup>10</sup> This is a (less) significant simplification again. My bad.  
<sup>11</sup> *"But it works on my machine!"*

---

**License**: This document is licensed under the **MIT License**. See the `LICENSE` file in the project root for full license details.
