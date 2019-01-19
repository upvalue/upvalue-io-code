import * as React from 'react';

import * as ReactDOM from 'react-dom';

import { computed, observable } from 'mobx';
import { observer } from 'mobx-react';

import { types } from 'mobx-state-tree';

const Todo = types.model({
  text: types.string
})

const Store = types.model({
  todos: types.array(Todo),
}).actions((self) => {
  return {
    // The typeof operator below is the important one: this is how you interact with types introduced
    // by mobx-state-tree
    add (todo: typeof Todo.Type) {
      self.todos.push(todo);
    },

    remove(todo: typeof Todo.Type) {
      // self.todos.remove(todo);

      // This is necessary to interact with Store.Type.todos, which is an IObservable array, not
      // a normal array, which is what filter returns.
      self.todos.replace(self.todos.filter((v, i) => {
        return v.text !== todo.text;
      }));
    },
  }
});

@observer
class App extends React.Component<{store: typeof Store.Type}> {
  todoInput: HTMLInputElement;

  addTodo(e: React.SyntheticEvent<HTMLButtonElement>) {
    e.preventDefault();
    if(this.todoInput.value !== '') {
      this.props.store.add({ text: this.todoInput.value });
      // Notice that this is type-checked properly. For example, something like this:
      // this.props.store.add({ tyxt: true });
      // Will result in a compile-time error
      this.todoInput.value = '';
    }
  }

  removeTodo(e: React.SyntheticEvent<HTMLButtonElement>, todo: typeof Todo.Type) {
    e.preventDefault();
    this.props.store.remove(todo);
  }

  render() {
    return <div>
      <form>
        <input ref={(r) => { if(r) this.todoInput = r; }} type="text" placeholder="Add entry" />
        <button type="submit" onClick={(e) => this.addTodo(e)}>Add todo</button>
      </form>

      <ul>
        {this.props.store.todos.map((item, i) => {
          return <li key={i}>
            {item.text} &nbsp; &nbsp;
            <button onClick={(e) => this.removeTodo(e, item)}>Remove</button>
          </li>
        })}
      </ul>

    </div>
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const store = Store.create({ todos: [] });
  ReactDOM.render(<App store={store} />, document.getElementById('root'));
});
