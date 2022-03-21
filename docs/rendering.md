## Inline Components {#inline-components}

The most basic way to render a Livewire component on a page is using the `<livewire:` tag syntax:

```jinja
<div>
    <livewire:show-posts />
</div>
```

Alternatively you can use the `@@livewire` blade directive:

```jinja
    @livewire('show-posts')
```

If you have a component inside a sub-folder with its own namespace, you must use a dot (`.`) prefixed with the namespace.

For example, if we have a `ShowPosts` component inside of a `app/Http/Livewire/Nav` folder, we would indicate it as such:

```jinja
    <livewire:nav.show-posts />
```

### Parameters {#parameters}

#### Passing Parameters

You can pass data into a component by passing additional parameters into the <code><livewire:</code> tag.

For example, let's say we have a `show-post` component. Here's how you would pass in a `$post` model.

```jinja
    <livewire:show-post :post="$post">
```

Alternatively, this is how you can pass in parameters using the Blade directive.

```jinja
    @livewire('show-post', ['post' => $post])
```

#### Receiving Parameters

Livewire will automatically assign parameters to matching public properties.

For example, in the case of @verbatim `<livewire:show-post :post="$post">` @endverbatim, if the `show-post` component has a public property named `$post`, it will be automatically assigned:

```python
class ShowPost(Component):
    post: Post

    ...
```

If for whatever reason, this automatic behavior doesn't work well for you, you can intercept parameters using the `mount()` method:

```python

class ShowPost(Component):
    title: str
    content: str

    def mount(self, post: Post):
        self.title = post.title
        self.content = post.content
```

```{note}

In Livewire components, you use <code>mount()</code> instead of a class constructor <code>__construct()</code> like you may be used to.

NB: <code>mount()</code> is only ever called when the component is first mounted and will not be called again even when the component is refreshed or rerendered.
```

Like a controller, you can inject dependencies by adding type-hinted parameters before passed-in ones.

```python
# use \Illuminate\Session\SessionManager;

class ShowPost(Component):
    title: str
    content: str

    def mount(self, session: SessionManager, post):
        session[f"post.{post.id}.last_viewed"] = time.now()

        self.title = post.title
        self.content = post.content

    ...
```

## Full-Page Components {#page-components}

If the main content of a page is a Livewire component, you can pass the component directly into a Laravel route as if it were a controller.

```python

Route::get('/post', ShowPosts::class);
```

By default, Livewire will render the `ShowPosts` component into the `@{{ $slot }}` of a blade layout component located at: `resources/views/layouts/app.blade.php`

```jinja
<head>
    @livewireStyles
</head>
<body>
    {{ $slot }}

    @livewireScripts
</body>
```

For more information on Laravel components, [visit Laravel's documentation](https://laravel.com/docs/blade#components).

### Configuring The Layout Component {#custom-layout}

If you want to specify a default layout other than the `layouts.app`, you can override the `livewire.layout` config option.

```
    'layout' => 'app.other_default_layout'
```

If you need even more control, you can use the `->layout()` method on the view instance you return from `render()`.


```python

class ShowPosts(Component):
    ...
    def render(self):
        return view('livewire.show-posts', layout="layouts.base")
```

If you are using a non-default slot in the component, you can also chain on `->slot()`:

```python

    def render(self)
        return view('livewire.show-posts')
            ->layout('layouts.base')
            ->slot('main');
```

Alternatively, Livewire supports using traditional Blade layout files with `@@extends`.

Given the following layout file:

@component('components.code')
@verbatim
<head>
    @livewireStyles
</head>
<body>
    @yield('content')

    @livewireScripts
</body>
@endverbatim
@endcomponent

You can configure Livewire to reference it using `->extends()` instead of `->layout()`:

@component('components.code', ['lang' => 'php'])
public function render()
{
    return view('livewire.show-posts')
        ->extends('layouts.app');
}
@endcomponent

If you need to configure the `@@section` for the component to use, you can configure that as well with the `->section()` method:

@component('components.code', ['lang' => 'php'])
public function render()
{
    return view('livewire.show-posts')
        ->extends('layouts.app')
        ->section('body');
}
@endcomponent

If you need to pass data from your components to your layout, you can pass the data along with the layout method:

@component('components.code', ['lang' => 'php'])
public function render()
{
    return view('livewire.show-posts')
        ->layout('layouts.base', ['title' => 'Show Posts'])
}
@endcomponent

In some cases you don't need to pass your layout name or you want to pass layout data separately, you can use layoutData method:

@component('components.code', ['lang' => 'php'])
public function render()
{
    return view('livewire.show-posts')
        ->layoutData(['title' => 'Show Posts'])
}
@endcomponent


### Route Parameters {#route-params}

Often you need to access route parameters inside your controller methods. Because we are no longer using controllers, Livewire attempts to mimic this behavior through its `mount` method. For example:

@component('components.code', ['lang' => 'php'])
Route::get('/post/{id}', ShowPost::class);
@endcomponent

@component('components.code', ['lang' => 'php'])
```python

class ShowPost(Component):
    post: Post

    def mount(self, post_id):
        self.post = Post.find(id)

    ...
```

As you can see, the `mount` method in a Livewire component is acting like a controller method would as far as its parameters go. If you visit `/post/123`, the `$id` variable passed into the `mount` method will contain the value `123`.


### Route Model Binding {#route-model-binding}

Like you would expect, Livewire components implement all functionality you're used to in your controllers including route model binding. For example:

@component('components.code', ['lang' => 'php'])
Route::get('/post/{post}', ShowPost::class);
@endcomponent

@component('components.code', ['lang' => 'php'])
class ShowPost extends Component
{
    public $post;

    public function mount(Post $post)
    {
        $this->post = $post;
    }
}
@endcomponent

If you are using PHP 7.4, you can also typehint class properties, and Livewire will automatically route-model bind to them. The following component's `$post` property will be automatically injected with no need for the `mount()` method.

@component('components.code', ['lang' => 'php'])
class ShowPost extends Component
{
    public Post $post;
}
@endcomponent


## The Render Method {#render-method}

A Livewire component's `render` method gets called on the initial page load AND every subsequent component update.

```{tip}
In simple components, you don't need to define a `render` method yourself. The base Livewire component class has a dynamic `render` method included.
```


### Returning Blade Views {#returning-blade}
The `render()` method is expected to return a Blade view, therefore, you can compare it to writing a controller method. Here is an example:

@component('components.warning')
Make sure your Blade view only has ONE root element.
@endcomponent

@component('components.code-component')
@slot('class')
@verbatim

class ShowPosts extends Component
{
    public function render()
    {
        return view('livewire.show-posts', [
            'posts' => Post::all(),
        ]);
    }
}
@endverbatim
@endslot
@slot('view')
@verbatim
<div>
    @foreach ($posts as $post)
        @include('includes.post', $post)
    @endforeach
</div>
@endverbatim
@endslot
@endcomponent

### Returning Template Strings {#returning-strings}
In addition to Blade views, you can optionally return a Blade template string from `render()`.

@component('components.code-component')
@slot('class')
@verbatim
class DeletePost extends Component
{
    public Post $post;

    public function delete()
    {
        $this->post->delete();
    }

    public function render()
    {
        return <<<'blade'
            <div>
                <button wire:click="delete">Delete Post</button>
            </div>
        blade;
    }
}
@endverbatim
@endslot
@endcomponent

```{note}

For inline components like above, you should use the <code>--inline</code> flag during creation: <code>artisan make:livewire delete-post --inline</code>
```
